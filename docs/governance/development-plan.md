# HALO: Development Plan (v0.1)

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-15

This plan describes how HALO v0.1 will be built, in what order, and how each step is verified. It contains no time estimates, because none have been measured. Progress is judged by exit criteria. Items marked **Proposed** await the owner's decision.

## 1. Order of work and a deviation from the specification

The project specification lists ten phases in sequence. HALO v0.1 must do something from several of them at once: sign in, analyse a number, save it, investigate, attach evidence, assess risk and summarise. So v0.1 is built as a **thin vertical slice** across those phases. The broader work in the specification's Phases 4 to 6 (external sources, full fraud intelligence, geospatial and relationships) continues after v0.1. **Proposed:** accept this ordering. It departs from the specification's literal sequence, and the owner must confirm it.

## 2. Milestones

| ID | Milestone | Exit criteria |
|---|---|---|
| M0 | Phase 0 documents complete | All Phase 0 documents committed; open decisions answered or consciously deferred; legal question list kept |
| M1 | Environment complete | Docker re-verified; PostgreSQL with PostGIS running in a container, bound to `127.0.0.1` only; connection verified from Windows |
| M2 | Foundation | Backend skeleton, configuration from environment variables, structured logging, health endpoint, first tests passing, minimal frontend scaffold, CI running |
| M3 | Identity and access | First migration (tenancy, identity, sessions, audit); Argon2id sign-in; server-side sessions; role checks; organisation separation; throttling; audit events; related tests passing (FR-01 to FR-04, FR-17, FR-18) |
| M4 | Phone analysis | Number parsing and validation with the lite library; structured result with source, limits and "Not available"; save as immutable record; tests with synthetic numbers (FR-05 to FR-09) |
| M5 | Investigations and evidence | Investigations, linked indicators, observations, evidence upload with hashes and event history (FR-10 to FR-13) |
| M6 | Risk and summary | Rule engine, assessment with reasons, review status, investigation summary (FR-14 to FR-16) |
| M7 | Interface for the main workflow | Sign in, analyse, save, investigate, attach, assess and summarise through the web interface; accessible by keyboard (NFR-06) |
| M8 | Verification and v0.1 release | Every acceptance criterion mapped to a passing test; security checks from the threat model run; backup and restore tested; secret and dependency scans clean; documentation updated; v0.1 tagged |

Each milestone ends with: tests run and results recorded, manual verification, `PROJECT_STATUS.md` updated, and an explicit pause for the owner to confirm before the next milestone begins.

## 3. First backlog, in order

1. Verify Docker and write a Docker Compose file for PostgreSQL only, loopback-bound, with the password in the git-ignored `.env` (M1).
2. Create the Python 3.14 virtual environment and pin dependencies, checking each licence at install (M2).
3. Backend skeleton, configuration, logging and health endpoint with tests (M2).
4. Alembic set up; first migration for tenancy, identity, sessions and audit, followed by the database accounts and append-only protections (M3).
5. Authentication, sessions, throttling and role checks, with organisation-scoped data access (M3).
6. Phone-analysis module with the lite library; verify that parsing, validity, region and number type work without carrier and geocoding data (M4).
7. Investigations, observations and evidence (M5).
8. Rule engine, assessments and summary (M6).
9. Frontend workflow (M7).
10. Hardening, test completion and release (M8).

## 4. Risk rules for v0.1 (Proposed)

v0.1 holds only numbering metadata and analyst-entered observations. The rules are therefore few and cautious. **Thresholds are uncalibrated starting values**, not findings from data, and are documented as such.

| Rule | Behaviour |
|---|---|
| Principle | **Number validity, number type and format never contribute to risk.** A mistyped or unusual number is not evidence of fraud. |
| RULE-00 (default) | If no rule has enough evidence, the result is **"Not assessed: insufficient information"**, not "Low". |
| RULE-01 corroborated reports | Count observations of class *public* or *user-submitted* that cite **distinct** sources, recorded within the last 180 days (starting value). 2 distinct sources: Guarded. 3 to 4: Elevated. 5 or more: High. |
| RULE-02 contradiction | If observations conflict (for example, one confirms the number is legitimate while others report fraud), no escalation occurs and the result is flagged "contradictory intelligence: human review required". |
| RULE-03 staleness | Observations older than the window do not count, and the result states that older material exists. |
| Critical | Reserved, **not reachable in v0.1**, because v0.1 has no authoritative evidence source. |
| Human review | Every assessment is a draft until a reviewer marks it reviewed. The summary is labelled as a draft for human review. |

Limits to state in the interface: HALO cannot verify that cited sources are independent or genuine, because it is relying on analyst-recorded citations. Every assessment says so.

## 5. Testing strategy

| Layer | Tool and focus |
|---|---|
| Unit | pytest: parsing, normalisation, rules, hashing |
| Database | Migrations apply and reverse on an empty database; constraints, append-only protections and cross-organisation integrity |
| API | Validation errors, authentication, role and organisation checks for each endpoint |
| Security | Threat-model items T1 to T18, each with an automated or documented manual check |
| Frontend | Component tests and a keyboard walk-through of the main workflow |
| Release | Backup and restore; secret scan; dependency scan; log inspection for sensitive data |

- Every acceptance criterion in `product-requirements.md` maps to at least one test (NFR-04).
- Test data is synthetic. Real numbers never enter the repository.
- CI runs the tests on every push using GitHub Actions. The free allowance for a private repository must be checked before relying on it.

## 6. Working practices

- **Branches (accepted 2026-11-15, DEC-011):** from M2, each development task is done on a short-lived feature branch and merged into `main` only after its tests pass and the work is verified. Documentation-only changes may go straight to `main`. Details are in `CONTRIBUTING.md`.
- **Commits:** small, with the conventional prefixes already in use (`docs:`, `chore:`, `feat:`, `fix:`, `test:`).
- **Verification gate:** before every `git add`, check that the file is saved and its path in `git status` is the expected one. Commit only after the expected check output has been confirmed.
- **Changes by script:** scripted edits must match each pattern exactly once and write nothing otherwise.
- **Dependencies:** each one's licence, account requirement and data flow are checked at install and recorded.
- **Status:** `PROJECT_STATUS.md` is updated at the end of every milestone.

## 7. Risks to this plan

| Risk | Mitigation |
|---|---|
| Only 7.7 GB of RAM, with Docker limited to about 3 GB | Docker runs PostgreSQL only; the backend and frontend run natively; measure memory before adding services |
| Python 3.14 compatibility surprises | Pin versions; verify installation on a throwaway environment first |
| One developer | Small milestones, automated tests and documented decisions |
| Legal review has not happened | v0.1 uses synthetic data only; no real data until review |
| Scope creep toward impressive features | The scope and requirements documents are the reference; additions need a recorded decision |
| Docker Desktop is proprietary | Keep Docker optional; keep the native PostgreSQL fallback documented |
| Library licences and behaviour differ from memory | Verify at install; record the results |

## 8. Definition of done (per feature)

1. The intended behaviour is written down.
2. The feature is implemented.
3. Automated tests pass, including invalid input and access-control cases where relevant.
4. Manual verification is recorded.
5. Documentation and `PROJECT_STATUS.md` are updated.
6. Remaining issues are listed.

## 9. Open decisions

- [ ] Accept the vertical-slice ordering in section 1?
- [ ] Accept the proposed v0.1 risk rules and starting thresholds in section 4, including "Not assessed: insufficient information"?
- [x] Feature branches from M2: accepted by the owner on 2026-11-15 (DEC-011).
- [ ] Is multi-factor authentication part of v0.1, or a later release?