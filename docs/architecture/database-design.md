# HALO: Initial Database Design (v0.1)

**Status:** Draft v0.1 (Phase 0). A design only; no migration exists yet.
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-13

This document turns `system-architecture.md` into tables, constraints and permissions for HALO v0.1. Items marked **Proposed** await the owner's review. Schema changes are made only through Alembic migrations, never by hand.

## 1. Conventions

- **Primary keys:** UUID, defaulting to `gen_random_uuid()` (built into recent PostgreSQL; verify against the installed version). The exception is `audit_events`, which uses a `bigint` identity so ordering is unambiguous.
- **Timestamps:** `timestamptz`, stored in UTC, `created_at` defaulting to `now()`.
- **Names:** `snake_case`, plural table names.
- **Enumerations:** `text` columns with `CHECK` constraints. They are easier to migrate than PostgreSQL enum types.
- **Free text:** length limits enforced with `CHECK` constraints.
- **No hard deletes of investigative records.** Records change `status`; physical deletion happens only through a documented retention job.
- **Tenancy:** every table holding organisation data has `organisation_id NOT NULL` with a foreign key.
- **Phone numbers** are stored in E.164 form. v0.1 development uses synthetic numbers only; real numbers never enter the repository or its tests.

## 2. Tables in v0.1

### 2.1 Tenancy and identity

| Table | Key columns | Constraints and notes |
|---|---|---|
| `organisations` | id, name, status (`active`/`suspended`), created_at | `name` unique. **Proposed:** a seeded `system` organisation holds the platform administrator. |
| `roles` | id, code, name, is_enabled | Seven seeded rows (section 6). `code` unique. `is_enabled` is false for roles not yet active. |
| `permissions` | id, code, description | `code` unique, for example `investigation.create`, `evidence.upload`, `user.manage`. |
| `role_permissions` | role_id, permission_id | Composite primary key; both are foreign keys. |
| `users` | id, organisation_id, email, display_name, password_hash, role_id, is_active, failed_login_count, locked_until, password_changed_at, mfa_enabled, mfa_secret_encrypted, created_at, last_login_at | **Proposed:** email stored lower-case and globally unique. Argon2id hash only; no password hints. One role per user in v0.1. MFA columns exist but stay unused until MFA is built. |
| `sessions` | id, user_id, token_hash, csrf_hash, created_at, last_seen_at, idle_expires_at, absolute_expires_at, revoked_at, revoked_reason | Only the **hash** of the 256-bit token is stored. `token_hash` unique. **Proposed:** no IP address or user-agent stored in v0.1, to minimise personal data. |

### 2.2 Intelligence

| Table | Key columns | Constraints and notes |
|---|---|---|
| `intelligence_sources` | id, code, name, source_type, reference, licence, reliability_class, created_at | The provenance registry, minimal in v0.1. `code` unique. Seeded with `phonenumbers_metadata`, `halo_rules`, `manual_entry`. Reliability is one of `authoritative`, `high`, `medium`, `low`, `unrated`. |
| `phone_indicators` | id, organisation_id, e164, country_calling_code, created_by, created_at | Unique on (`organisation_id`, `e164`). `CHECK (e164 ~ '^\+[1-9][0-9]{6,14}$')`. |
| `phone_analyses` | id, organisation_id, phone_indicator_id, submitted_text, result (jsonb), library_name, library_version, source_id, info_class, analysed_by, analysed_at, stale_after | **Immutable:** a new analysis is a new row. `result` follows the structure in section 12 of the architecture (value, class, source, timestamp, confidence, limitations). `info_class` is one of the classes in `scope-and-boundaries.md`. `submitted_text` is length-limited. **Proposed:** keep it, since it is useful for debugging and is already sensitive data under the same controls. |

### 2.3 Investigations and evidence

| Table | Key columns | Constraints and notes |
|---|---|---|
| `investigations` | id, organisation_id, reference, title, summary, status, created_by, created_at, closed_at | `reference` unique per organisation (for example `HALO-2026-0001`). `status` in (`open`, `in_review`, `closed`). |
| `investigation_indicators` | organisation_id, investigation_id, phone_indicator_id, added_by, added_at | Primary key (`investigation_id`, `phone_indicator_id`). |
| `observations` | id, organisation_id, investigation_id, body, info_class, source_id, created_by, created_at, superseded_by | **Append-only in practice:** an edit inserts a new row and sets `superseded_by` on the old one. History is never lost. |
| `evidence_items` | id, organisation_id, investigation_id, original_filename, stored_name, size_bytes, declared_type, detected_type, sha256, data_class, status, uploaded_by, uploaded_at | `sha256` is a 64-character lower-case hex string (`CHECK`). `data_class` in (`synthetic`, `authorised`). `status` in (`active`, `withdrawn`). File content is never edited; `stored_name` is random, never the uploaded name. |
| `evidence_events` | id, organisation_id, evidence_item_id, event_type, actor_id, reason, occurred_at | **Append-only.** Records ingest, verification, access and withdrawal. |

### 2.4 Risk and audit

| Table | Key columns | Constraints and notes |
|---|---|---|
| `risk_assessments` | id, organisation_id, phone_indicator_id, phone_analysis_id, investigation_id (nullable), classification, ruleset_version, reasons (jsonb), limitations, status, reviewed_by, reviewed_at, created_at | `classification` in (`low`, `guarded`, `elevated`, `high`, `critical`). `status` in (`draft`, `human_reviewed`, `withdrawn`). `CHECK (status <> 'human_reviewed' OR (reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL))`. `reasons` lists every rule that fired and its evidence reference. |
| `audit_events` | id (bigint identity), occurred_at, organisation_id (nullable), actor_user_id (nullable), action, target_type, target_id, outcome, details (jsonb), request_id | **Append-only.** `outcome` in (`success`, `failure`, `denied`). Stores identifiers, never full phone numbers, tokens or passwords. Not given an ON DELETE rule that could remove history; users are deactivated, never deleted. |

## 3. Cross-organisation integrity

Application filters can have bugs, so the database enforces the boundary too. Each parent table that organisation data points at gets a unique constraint on (`organisation_id`, `id`). Each child references **both columns**:

```sql
-- Illustration only; the real definition will be written as an Alembic migration.
ALTER TABLE investigations
  ADD CONSTRAINT investigations_org_id_uniq UNIQUE (organisation_id, id);

ALTER TABLE investigation_indicators
  ADD CONSTRAINT inv_ind_investigation_fk
  FOREIGN KEY (organisation_id, investigation_id)
  REFERENCES investigations (organisation_id, id);
```

A row in organisation A then cannot reference a record in organisation B, even through a bug. **Proposed second layer, to evaluate:** PostgreSQL row-level security.

## 4. Append-only enforcement and database accounts

Two layers, because either could fail alone:

1. **Privileges.** Two database accounts: `halo_owner` runs migrations; `halo_app` is what the application uses. `halo_app` has no DDL rights. On `audit_events` and `evidence_events` it has `INSERT` and `SELECT` only. Passwords are chosen by the owner and kept in the git-ignored `.env`.
2. **Triggers (proposed).** A trigger on each append-only table raises an error on `UPDATE` or `DELETE`. It protects against accidental over-granting of privileges.

## 5. Indexes (starting set)

- Foreign-key columns used in joins and tenant filters: (`organisation_id`, plus the parent column) on every child table.
- `users`: unique on lower-case email.
- `sessions`: unique on `token_hash`; an index on `absolute_expires_at` for cleanup.
- `phone_indicators`: unique on (`organisation_id`, `e164`).
- `audit_events`: indexes on (`organisation_id`, `occurred_at`) and (`actor_user_id`, `occurred_at`).
- Indexes are added when a real query needs them, and checked with `EXPLAIN`, not guessed.

## 6. Seed data

- **Roles:** `platform_admin` (not enabled), `org_admin` (enabled, **Proposed**), `investigator` (enabled), `analyst`, `researcher`, `reviewer` (not enabled), `read_only` (enabled).
- **Intelligence sources:** `phonenumbers_metadata`, `halo_rules`, `manual_entry`.
- **Platform administrator:** created only by a local setup script, never by a web endpoint.
- No sample users or passwords are seeded. Synthetic demo data comes later through a separate, clearly labelled generator.

## 7. Retention (Proposed starting values)

These are engineering defaults, and **a South African legal professional must review them** before any real data is held.

| Data | Starting rule |
|---|---|
| Expired or revoked sessions | Deleted 30 days after expiry |
| `phone_analyses` | Marked stale after 90 days (`stale_after`); never silently deleted |
| `audit_events` | Kept; retention period to be set with legal advice |
| Evidence and investigations | Retained until the investigation owner and legal review decide otherwise |

## 8. Deferred tables

| Table | Deferred to | Reason |
|---|---|---|
| `enrichment_results` | Phase 4 | Needs the source registry and connectors |
| `device_indicators` | Device module | Synthetic-data research only |
| `relationships` | Phase 6 | Needs more than one indicator type |
| `consent_records` | Phase 5 | Needed only when user-submitted reports exist |
| `intelligence_reports` | Later | v0.1 generates the investigation summary on demand rather than storing it (**Proposed**) |
| Geospatial tables | Phase 6 | Needs PostGIS and a precision policy |

## 9. How the design will be verified

Each item becomes an automated test once the migration exists:

- Migrations apply cleanly to an empty database and reverse cleanly.
- Inserting a child row that references another organisation's parent is rejected.
- `UPDATE` and `DELETE` on `audit_events` and `evidence_events` fail for `halo_app`.
- An invalid E.164 value is rejected.
- Marking a risk assessment `human_reviewed` without a reviewer is rejected.
- `halo_app` cannot create, alter or drop tables.

## 10. Open decisions

- [ ] Email globally unique, or unique per organisation?
- [ ] A seeded `system` organisation for the platform administrator.
- [ ] One role per user in v0.1.
- [ ] Keep `submitted_text` in `phone_analyses`.
- [ ] Trigger-based append-only protection in addition to privileges.
- [ ] Evaluate row-level security.
- [ ] Retention values in section 7 (subject to legal review).
- [ ] Summaries generated on demand, not stored.