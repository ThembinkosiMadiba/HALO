# HALO: Decision Register

**Status:** Draft v0.1
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-15

Each significant decision is recorded with its date, status and reason. A decision is changed by adding a new entry that supersedes the old one, never by editing history.

## Summary

| ID | Decision | Date | Status |
|---|---|---|---|
| DEC-001 | Use Python 3.14, not 3.15, for HALO's virtual environment | 2026-11-11 | Accepted |
| DEC-002 | Modular monolith; Docker is a convenience, not a dependency | Project specification | Accepted |
| DEC-003 | GitHub repository stays private until a pre-publication review | 2026-11-12 | Accepted |
| DEC-004 | LF line endings everywhere except `.bat`, `.cmd` and `.ps1` | 2026-11-11 | Accepted |
| DEC-005 | Model all seven roles; enable only organisation administrator, investigator and read-only in v0.1 | 2026-11-13 | Accepted (the reading of "administrator" as organisation administrator awaits explicit confirmation) |
| DEC-006 | Defer user-submitted reports to Phase 5 | 2026-11-13 | Accepted |
| DEC-007 | Session, evidence-storage and MFA defaults as set out in `system-architecture.md` | 2026-11-13 | Proposed, awaiting owner review |
| DEC-008 | Use the lite build of the phone-number library for v0.1 | 2026-11-14 | Accepted |
| DEC-009 | Run PostgreSQL from the `postgis/postgis:18-3.6` image (PostgreSQL 18.6); digest recorded | 2026-11-15 | Accepted |
| DEC-010 | Start the database clean; enable extensions only through migrations (initdb mount) | 2026-11-15 | Accepted and verified |
| DEC-011 | Short-lived feature branches from M2; documentation-only fixes may go directly to `main` | 2026-11-15 | Accepted |
| DEC-012 | Backend dependency set (28 pinned packages); SQLAlchemy 2.0 pin proposed after Smart App Control blocked 2.1.8 | 2026-11-15 | Verified; SQLAlchemy part proposed |

## DEC-001: Python 3.14 for HALO

- **Context:** Python 3.15.2 was installed, but prebuilt wheels for key libraries on 3.15 were only starting to appear, and a missing wheel means building from source on Windows.
- **Decision:** Build HALO's virtual environment on Python 3.14.10. Python 3.15 stays installed and untouched.
- **Revisit:** When the full dependency set is confirmed to install cleanly on 3.15.

## DEC-008: Lite build of the phone-number library

- **Date:** 2026-11-14
- **Decision:** HALO v0.1 uses `phonenumberslite`, not the full `phonenumbers` package.
- **Context:** Mobile number portability means an original number prefix does not show which carrier a subscriber is on today. HALO's priorities are accuracy, reliability, explainability and avoiding misleading intelligence.
- **Reasons for excluding the full package:**
  - The full package bundles carrier and geocoding data. A number's prefix would let HALO name a carrier or a place that may be wrong for a ported or relocated number.
  - Leaving the data out makes that misleading output impossible. Relying on every future developer to avoid calling it is weaker.
  - Anything shown in an investigation can be treated as intelligence, so a plausible but unverifiable "carrier" label is a real harm.
- **What the lite build excludes (per the package documentation):** carrier, geocoding and timezone metadata.
- **What it is expected to keep (to be verified at install):** parsing, formatting, possible and valid checks, region, and number type from the core metadata.
- **Limitations and consequences:**
  - v0.1 cannot show a carrier name, a place description or a time zone for any number. The interface shows "Not available" for these.
  - A valid number is not proof that it is assigned, active or currently on any particular network.
  - Number type comes from numbering metadata and is not a live status. This is to be documented accurately in the interface.
- **Packaging rule:** do not install the full and lite packages in the same environment. They are expected to share one import name, to be verified at install.
- **Alternatives considered:** the full package with the carrier functions unused (rejected: the data would still be present); a custom South African range table (rejected for now: it needs the ICASA regulations read first, and the licence terms checked).
- **Revisit when:** a reliable, authoritative and legally usable source for current carrier or geographic data exists. Any such source needs its own register entry, a threat-model update and a legal check before use.
- **Verification owed:** at install time, check the licence and NOTICE file, record the exact version, and confirm parsing, validity, region and number type work without the excluded data.

## DEC-009: Database image and version

- **Date:** 2026-11-15
- **Decision:** Run PostgreSQL from the `postgis/postgis:18-3.6` image through Docker Compose.
- **Verified facts (command output):** PostgreSQL 18.6 (Debian 18.6-1.pgdg13+2); PostGIS 3.6.4 binaries available; 959 MB on disk; digest `sha256:4a43e3c3e5d55b9208240fc71db543b79c638766280c625a425bd0a2390989c4`.
- **Tag and digest:** The Compose file uses the rolling tag `18-3.6`. The digest above records the image that was verified. It is recorded for comparison and is **not enforced**. **Proposed:** pin by digest before any shared deployment.
- **Reasons:** current PostgreSQL major version at the time; the image is maintained by the PostGIS project according to its repository README; no native PostgreSQL install is needed; the PostGIS binaries are present for Phase 6, so the image does not have to be swapped under live data.
- **Compose settings (verified):** published on `127.0.0.1` only; password required from the git-ignored `.env`; `restart: "no"`; memory ceiling 1 GiB; data volume mounted at `/var/lib/postgresql`, the path used by PostgreSQL 18 images.
- **Measured cost:** the container used about 65 MiB and the Docker VM about 223 MB with an idle database.
- **Known limitations:** Docker Desktop is proprietary; the licences of the image contents were **not verified**; the bootstrap role is a superuser (threat T19); local connections inside the container use `trust` (threat T20).
- **Revisit when:** a PostgreSQL or PostGIS security release requires a new image. Then update the digest deliberately and re-run the baseline verifier and the tests.

## DEC-010: Clean database start; extensions only through migrations

- **Date:** 2026-11-15
- **Decision (owner, Option B):** Replace the image first-run script so a new database contains only the default `plpgsql` extension. PostGIS and any other extension are enabled only by version-controlled Alembic migrations.
- **Context:** The first start of the image enabled five extensions without HALO asking for it. Its script `10_postgis.sh` also created a `template_postgis` database.
- **State before the change (verified):** extensions `fuzzystrmatch`, `plpgsql`, `postgis`, `postgis_tiger_geocoder`, `postgis_topology`; schemas `public` (1 table), `tiger` (34) and `topology` (2), so 37 tables, and 56 relations outside system schemas including views and sequences; `spatial_ref_sys` held 8,500 rows; databases `halo`, `postgres`, `template0`, `template1`, `template_postgis`; one role, `halo_owner`, a superuser.
- **Options considered:** (A) accept the image defaults; (B) mount an empty folder over the init directory; (C) drop the extra extensions by hand. C was rejected because a rebuilt volume would bring them back.
- **Implementation:** `docker-compose.yml` mounts `infrastructure/docker/initdb` read-only over `/docker-entrypoint-initdb.d`. The folder holds only a README, which the entrypoint ignores.
- **Safety before deletion (verified):** the volume was created the same day; one container used it; the repository held no migrations or application code; the reset script counted 0 relations not owned by an extension.
- **Verification after recreation, 2026-11-15 (verified):** `scripts/verify-database-baseline.ps1` passed all six checks. The start-up log shows `ignoring /docker-entrypoint-initdb.d/README.md` and no PostGIS loading line. A query returned: `spatial_ref_sys` absent, one extension, no `tiger` or `topology` schema. The image digest was unchanged.
- **Negative control (verified):** run against the old database, the verifier reported four failures (extensions, schemas, 56 relations, extra template database), so it detects the unwanted state.
- **Reproducibility:** a fresh volume plus the committed Compose file produces the same state with no manual cleanup. `scripts/reset-database.ps1` recreates the volume. It refuses to proceed if the database holds objects that are not part of an extension, and it requires typing DELETE.
- **Limitations:** the verifier describes the state **before the first migration** and is expected to fail afterwards. It is not a regression test for later work. Verified on restart (2026-11-15): with data already in the volume, the log shows "Skipping initialization", so the image does not re-run its first-run scripts on an existing volume.
- **Consequences:** a migration must enable PostGIS when the geospatial module needs it. The binaries stay installed in the image. That migration needs a privileged role, which interacts with restricting `halo_owner` (open item).
- **Revisit when:** the geospatial module starts, or the image is replaced.

## DEC-011: Short-lived feature branches from M2

- **Date:** 2026-11-15
- **Decision (owner):** From M2 onward, each development task is done on a short-lived feature branch. A branch is merged into `main` only after the relevant tests pass and the implementation has been verified. Documentation-only fixes may still go directly to `main`.
- **Context:** Up to M1 every commit went straight to `main`. Several mistakes in this project were found only after committing (an empty file committed, a commit message describing content it did not contain). From M2 there is code, and `main` should stay stable.
- **Documentation-only means:** files under `docs/`, and `README.md`, `CONTRIBUTING.md` and `PROJECT_STATUS.md`. Anything else, including scripts, Compose, ignore rules and dependency files, needs a branch.
- **Before the automated test suite exists:** "tests pass" means the verification checks listed for the task were run and their output recorded.
- **Details:** `CONTRIBUTING.md`.
- **Merge method:** **Proposed**, not decided: local `git merge --no-ff`, then push. Revisit when automated checks run on GitHub.
- **Not verified:** whether GitHub branch protection is available for this private repository. Nothing relies on it.
- **Revisit when:** automated checks run on GitHub, or a second contributor joins.

## DEC-012: Backend dependency set and the Smart App Control finding

- **Date:** 2026-11-15
- **Status:** the dependency set is **verified**. The SQLAlchemy part is **Proposed** and awaits the owner.
- **Decision (verified):** the backend environment uses Python 3.14.10 and the 28 packages pinned in `backend/requirements.txt`, installed with `--only-binary=:all:`. Details and declared licences: `docs/research/dependency-register.md`.
- **Verified results:** `pip check` clean; installed set equals the file; all modules import; `psycopg` uses its binary implementation. A rebuild from the file reproduced the environment, using pip cache.
- **Finding: Smart App Control blocked a compiled file.** SQLAlchemy 2.1.8 installed, but `import sqlalchemy` failed with "An Application Control policy has blocked this file" for `sqlalchemy/sql/_util_cy.cp314-win_amd64.pyd`. Code Integrity events 3077 and 3033, logged 2026-11-15 11:37:35, say the file did not meet the Enterprise signing level requirements. Other compiled files (`pydantic_core`, `psycopg_binary`) loaded normally. Both the blocked file and `pydantic_core` are reported as unsigned, so signing does not explain the difference. The cause is not established.
- **Test in a throwaway environment (verified):** SQLAlchemy 2.0.57 imports and runs a query, reports compiled extensions as not in use, and Windows blocked `cyextension/immutabledict.cp314-win_amd64.pyd`. The library fell back to pure Python. Argon2 (with cffi bindings), MarkupSafe and greenlet loaded, and Argon2 produced an argon2id hash.
- **Proposed:** pin SQLAlchemy to `>=2.0,<2.1` (2.0.57 verified) when it is first needed in M3. Do not install SQLAlchemy in M2, which needs only `psycopg` for its connection test. Do not use 2.1.x until Windows accepts its compiled file or a reason appears.
- **Standing rule:** Smart App Control and similar protections are not to be turned off or excluded to make a package work.
- **Options considered:** (A) SQLAlchemy 2.1.8 built from source with the extensions disabled; (B) an older 2.0.x wheel; (C) defer SQLAlchemy to M3. C was chosen for M2 and B was tested for M3. A was not tested, because it would run a package build script on this machine.
- **Consequence for deployment:** any Windows machine enforcing Smart App Control or a similar policy may block compiled extensions. The installation guide must say so.
- **Not done:** hash pinning; release-age checks; vulnerability scan; Alembic tested with SQLAlchemy 2.0.57; licences read for SQLAlchemy 2.0.57, Argon2, phonenumberslite and Alembic.
- **Licence notes:** psycopg and psycopg-binary declare LGPL-3.0-only and certifi declares MPL-2.0. See the dependency register.
- **Revisit when:** M3 begins, a dependency is added, or Windows accepts the SQLAlchemy 2.1 files.
