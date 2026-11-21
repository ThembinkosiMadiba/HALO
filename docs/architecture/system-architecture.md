# HALO: System Architecture (v0.1)

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-21

This document describes how HALO v0.1 is structured and why. Items marked **Proposed** await the owner's review. Nothing described here is implemented yet. It should be read with `docs/governance/scope-and-boundaries.md` and `docs/security/threat-model.md`.

## 1. Architectural style

HALO is a **modular monolith**: one backend application, one database, one deployable unit, with strict internal module boundaries.

- Each module owns its own tables and exposes a small service interface. Modules do not query one another's tables directly.
- Cross-module calls go through those service interfaces only. This keeps modules separable later, if there is a genuine engineering reason, without paying the cost of microservices now.
- Complexity is added only when a requirement demands it. Redis, Celery and PostGIS are deferred until the features that need them.

## 2. Logical view

```
Browser (React + TypeScript)
        |  HTTPS (later) / loopback HTTP (v0.1 local)
        v
FastAPI application  -- /api/v1 --
   |-- Authentication and session handling
   |-- Authorisation (role + organisation checks)
   |-- Audit logging
   v
Modules (service interfaces)
   phone_intelligence   fraud_detection   investigations
   enrichment (later)   device_intelligence (later)
   geospatial (later)   relationships (later)
        |
        v
PostgreSQL (PostGIS enabled when geospatial work begins)
        |
Evidence files on a dedicated local directory (outside the repository)
```

## 3. Module map

| Module | v0.1 | Responsibility |
|---|---|---|
| core (auth, sessions, RBAC, audit, config) | Yes | Cross-cutting security, built first |
| phone_intelligence | Yes | Parse and validate numbers; report metadata, source, limits |
| investigations | Yes (minimal) | Investigations, indicators, observations, evidence metadata, summary |
| fraud_detection | Yes (minimal) | Explainable rule-based initial risk assessment |
| enrichment | No | Source registry and OSINT connectors (Phase 4) |
| device_intelligence | No | IMEI/TAC research on synthetic data |
| geospatial | No | PostGIS and map data |
| relationships | No | Relationship graph |

## 4. v0.1 request flow: analyse a number

1. Browser sends an authenticated request with the submitted number.
2. API validates the session, the CSRF token and the role.
3. `phone_intelligence` parses the number with a maintained library and returns structured fields. All metadata is local, with no network call.
4. The result is labelled with its information class, source, library version, timestamp and limitations. Unavailable fields are shown as "Not available".
5. If the user saves it, the record is stored under their organisation, linked to an investigation if chosen, and an audit event is written.
6. `fraud_detection` evaluates the stored record against the documented rules and returns a classification **with the rules that fired**.

## 5. Roles and organisation separation

All seven roles are defined in the database from the start.

| Role | v0.1 |
|---|---|
| Platform administrator | Modelled, **not enabled**. Created only by a local setup script, never through the web interface. |
| Organisation administrator | **Enabled** (**Proposed** interpretation of "administrator") |
| Investigator | **Enabled** |
| Intelligence analyst | Modelled, not enabled |
| Researcher | Modelled, not enabled |
| Reviewer | Modelled, not enabled |
| Read-only user | **Enabled** |

Rules:

- Every table that holds organisation data has an `organisation_id`. The server derives the organisation from the session and never trusts a client-supplied one.
- All data access goes through one organisation-scoped query helper, so that forgetting the filter is hard to do by accident.
- Authorisation is enforced in the API for each endpoint. Hiding buttons in the interface is not a control.
- **Proposed hardening, to evaluate:** PostgreSQL row-level security as a second layer behind the application filter.

## 6. Sessions and authentication (Proposed)

| Decision | Choice | Reason |
|---|---|---|
| Session type | Server-side sessions stored in PostgreSQL | Immediate revocation, no secrets in the browser, simple to audit |
| Session token | Random 256-bit value in an HttpOnly cookie; only its hash is stored | A database leak does not expose live tokens |
| Cookie flags | HttpOnly, SameSite=Lax, Secure whenever served over HTTPS (localhost behaviour to be tested) | Limits theft and cross-site use |
| CSRF | SameSite plus a per-session token on state-changing requests | Defence in depth |
| Lifetimes | 30 minutes idle, 8 hours absolute (starting values, adjustable) | Limits exposure of an unattended session |
| Invalidation | On logout, on password change, and by an administrator | Revocation that signed tokens cannot offer simply |
| Passwords | Argon2id; minimum length enforced; no password hints | As specified |
| Throttling | Progressive delay and temporary lockout; identical error for unknown user and wrong password | Reduces guessing and account enumeration |
| MFA | TOTP-based. Schema supports it from day one. **Proposed:** optional in v0.1, required for administrators before any non-local deployment | Security without blocking the first release |

Signed tokens (JWT) are not proposed for v0.1. They are harder to revoke, and the application does not need stateless scaling.

## 7. Evidence storage (Proposed)

- **Files** are stored on the local filesystem in a configured directory **outside the repository and the web root**, named by a random identifier, never by the uploaded filename.
- **Metadata** is stored in PostgreSQL: original filename, size, declared and detected type, SHA-256 hash, uploader, timestamp, investigation, and a data-class label (synthetic or authorised).
- **Hashing:** SHA-256 computed by the server on receipt and re-verified when the file is read.
- **Immutability:** content is never edited or overwritten. A correction is a new item. "Withdrawal" is a status change with a reason, recorded in an append-only evidence history.
- **Limits:** a file-size cap and an allow-list of types (starting values: PDF, PNG, JPEG, plain text, CSV; 10 MB). Files are served as attachments with content sniffing disabled, and never executed or rendered inline.
- **Malware scanning:** not in v0.1. An open-source scanner may be researched later, and it has not been evaluated.
- **Encryption at rest:** application-level encryption is deferred. Device-level encryption status on the host is checked during hardening, and nothing is claimed about it yet.
- **Trade-off:** two stores (database and filesystem) must be backed up together. Hash verification detects a mismatch after a restore.

## 8. Audit logging

- An append-only `audit_events` table records sign-ins, failures, role changes, investigation and evidence actions, exports and administrative changes.
- The application's database account has insert and select rights only, with no update or delete.
- Events reference record identifiers rather than copying sensitive values such as full phone numbers.
- **Proposed, later:** chain each event to the hash of the previous one, for tamper evidence.

## 9. Configuration, secrets and network exposure

- Configuration is read from environment variables, with a committed `.env.example` and a git-ignored `.env`. No secret is ever committed.
- The database and API bind to `127.0.0.1` only. Docker port mappings use the loopback address explicitly.
- No default or shared passwords. Setup requires the owner to choose them.
- Error responses to clients are generic. Logs are structured and redacted: no tokens, passwords or full numbers.

## 10. Deployment for v0.1

- **Local first.** Backend and frontend run natively on Windows. Docker is used for PostgreSQL only, as the machine has 7.7 GB of RAM and Docker is limited to about 3 GB. A native PostgreSQL install remains the fallback, so Docker is a convenience and not a dependency.
- **Later:** a Docker Compose file for the whole stack, then a cloud design (HTTPS, private networking, backups, monitoring) with its own threat model.
- **No external network calls in v0.1.** Core analysis works offline.

## 10.1 Database container and clean start

- **Image:** `postgis/postgis:18-3.6`, PostgreSQL 18.6, PostGIS 3.6.4 binaries, digest `sha256:4a43e3c3e5d55b9208240fc71db543b79c638766280c625a425bd0a2390989c4` (decision DEC-009).
- **Container settings:** published on `127.0.0.1` only. This was verified from Docker's own port record, and a connection to the machine's Wi-Fi address was refused. The password comes from the git-ignored `.env`. Restart policy is `no`, and the memory ceiling is 1 GiB.
- **Problem found on first start:** the image's own first-run script enabled `postgis`, `postgis_topology`, `fuzzystrmatch` and `postgis_tiger_geocoder`, created a `template_postgis` database, and added 37 tables (56 relations) plus 8,500 rows of reference data. That conflicts with the rule that schema changes come only from migrations.
- **Decision (DEC-010):** mount `infrastructure/docker/initdb` read-only over `/docker-entrypoint-initdb.d`. The folder holds only a README, which the image ignores.
- **Verified result, 2026-11-15:** after recreating the volume, the database has only `plpgsql`, only the `public` schema, no relations, no `template_postgis`, and one role. The PostGIS binaries remain installed, so a later migration can enable the extension.
- **Reproducibility:** `scripts/verify-database-baseline.ps1` (read-only) checks the starting state. `scripts/reset-database.ps1` (destructive, guarded) recreates the volume and runs the verifier.
- **Limit:** the verifier covers the pre-migration state only. After the first Alembic migration it is expected to fail, and migration tests take over.
- **Accounts:** `halo_owner` is the image bootstrap account and a superuser. The application must never use it (threat T19). Local connections inside the container use `trust` (threat T20).
- **Open:** how the migration that enables PostGIS obtains the privilege it needs while the application account stays non-superuser.

## 10.2 Backend skeleton (M2)

- **Location:** `backend/app`. Modules: `core/config.py` (settings), `core/logging_config.py` (logging), `api/health.py` (health check) and `main.py` (application factory). `backend/run_dev.py` starts the server.
- **Settings:** read from `HALO_*` environment variables and the repository `.env`. Safe defaults: environment `production` (API documentation hidden), loopback host, port 1024 or above. A non-loopback `api_host` is rejected at start-up. The database password is a secret type that does not appear in `repr`, `str` or model dumps. The application does not read the `POSTGRES_*` variables.
- **Logging:** a filter replaces the configured database password in log messages with `[REDACTED]`. Limits: it covers messages only, not exception tracebacks, and it knows only the configured password.
- **Endpoints:** `GET /api/v1/health` returns `{"status": "ok"}` and nothing else. It is public by design (section 12 allows only health check and login without authentication).
- **Responses:** `X-Content-Type-Options: nosniff` and `Cache-Control: no-store`. Unhandled errors return a generic 500 and log only the exception type. `/docs`, `/redoc` and `/openapi.json` exist only when the environment is `development`.
- **Not yet present:** authentication, authorisation, any database use by the application, a CORS policy, TLS (loopback HTTP only), rate limiting and a content-security policy.
- **Tests:** 15 unit tests (`pytest backend`) and 3 integration tests that need the database container (`pytest backend -m integration`). The integration tests use the database owner account as a documented exception (DEC-013, proposed).
- **Verified 2026-11-15:** all 18 tests pass. The real server, started in production mode, reported `127.0.0.1:8000` in its start-up log, answered the health check over loopback with the expected headers, returned 404 for `/docs`, and a connection to the machine's Wi-Fi address on port 8000 failed.
- **Limits of that verification:** a firewall could also have refused the Wi-Fi connection. Windows listener tools showed no listeners for either the API or the database container on this machine, so they were not used as evidence. Development mode was tested in-process only.

## 10.3 Continuous integration (written, not yet run on GitHub)

- **Workflow:** `.github/workflows/backend-tests.yml`, decision DEC-015 (proposed).
- **What it does:** on every push, on a Linux runner, installs the pinned dependencies from prebuilt wheels, compiles every Python file with syntax warnings treated as errors, and runs the 15 unit tests.
- **What it does not do:** run the integration tests (they need the database container), test on Windows, scan dependencies, or check licences.
- **Security:** read-only token, no persisted credentials, no secrets, third-party actions pinned to commit SHAs.
- **Why it matters here:** the local machine enforces Smart App Control, which blocked compiled libraries twice (DEC-012 and DEC-014). A Linux run is independent of that.
- **Status:** the first run on GitHub has not happened. This section is updated when it has.

## 11. Technology choices

Licences are from memory and **must be verified when each dependency is installed**. "Account" and "external data" apply to the running product.

| Technology | Role | Licence (verify) | Free and open source | Sends data out |
|---|---|---|---|---|
| Python 3.14 | Language | PSF | Yes | No |
| FastAPI, Pydantic | API and validation | MIT | Yes | No |
| SQLAlchemy, Alembic | ORM and migrations | MIT | Yes | No |
| phonenumberslite | Number parsing, validation and number type (no carrier, geocoding or timezone data) | Apache-2.0 (verify) | Yes | No (metadata bundled) |
| argon2-cffi | Password hashing | MIT | Yes | No |
| pytest | Testing | MIT | Yes | No |
| PostgreSQL | Database | PostgreSQL licence | Yes | No |
| PostGIS | Geospatial (later) | GPL-2.0-or-later | Yes | No |
| React, Vite, Tailwind CSS | Frontend | MIT | Yes | No |
| Leaflet, Cytoscape.js | Maps and graphs (later) | BSD-2, MIT | Yes | Map tiles would be a separate decision |
| Docker Desktop | Containers | Proprietary freeware; free for personal and small-business use | No | Pulls images from the internet |
| Redis, Celery | Background jobs | **Not in v0.1** (Redis licensing has changed over time; review before adopting) | n/a | n/a |

## 11.1 Decision: use the lite build of the phone-number library

HALO v0.1 uses `phonenumberslite`, not the full `phonenumbers` package (decision DEC-008, 2026-11-14).

- **Included (to verify at install):** parsing, formatting, possible and valid checks, region, and number type, from the core metadata.
- **Excluded:** carrier, geocoding and timezone metadata.
- **Why:** with mobile number portability, an original number prefix does not show which carrier a subscriber is on today. Leaving the carrier and geocoding data out makes that misleading output impossible, instead of relying on every future developer not to call it.
- **Consequence:** v0.1 cannot show a carrier name, a place description or a time zone for a number. The interface shows "Not available" for them.
- **Not both:** never install the full and lite packages in one environment. They are expected to share one import name (verify at install).
- **Revisit:** only when reliable, authoritative and legally usable data exists, with its own register entry and a threat-model update.

## 12. API conventions

- REST under `/api/v1`, with OpenAPI generated by FastAPI.
- Every endpoint requires authentication except health check and login.
- Input validated by Pydantic schemas. Responses use explicit schemas, never raw database rows.
- A single structure for analysis results: value, information class, source, timestamp, confidence, limitations.

## 13. Open decisions

- [ ] Owner to confirm: "administrator" means organisation administrator, platform administrator not enabled (section 5).
- [ ] Owner to review the session defaults and lifetimes (section 6).
- [ ] Owner to review evidence limits and allowed types (section 7).
- [ ] Whether to evaluate row-level security (section 5).
- [ ] Software licence for HALO.
- [x] Phone-number library build: lite (section 11.1, DEC-008).
- [ ] How the migration that enables PostGIS obtains a privileged role (section 10.1).
