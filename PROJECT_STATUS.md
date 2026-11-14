# HALO: Project Status

Resume point for development sessions. Update at the end of every milestone.
Only verified facts are recorded as facts; everything else is marked as open.

**Last updated:** 2026-11-15
**Current phase:** Phase 0 documents are drafted. Milestone M1 (database) is complete except an SQL login through the published port from Windows, which needs a database driver (M2).
**Next milestone:** M2 (backend foundation), after the open decisions that block it are answered

## Environment (verified from command output)

| Component | Verified state |
|---|---|
| OS | Windows 11 Home Single Language, build 26300, 64-bit |
| Hardware | Intel Core i5-12450H, 12 logical processors, 7.7 GB RAM, about 405 GB free on C: |
| Virtualisation | Working (hypervisor detected, virtualisation-based security running). The WMI flag showed `False` and was misleading. |
| Git | 2.56.1; `core.autocrlf=true` set system-wide; global `init.defaultBranch=main` |
| Python for HALO | **3.14.10**, installed with the Python Install Manager (`pymanager`); command `python3.14` |
| Other Python | 3.15.2 also installed. Not used for HALO yet because library wheel coverage for 3.15 was still arriving. |
| pip | 26.2.2; a throwaway virtual environment was created and removed successfully |
| Node.js / npm | v26.13.0 / 11.20.0. The published schedule puts Node 26 in Active LTS from 28 Oct 2026; the `process.release.lts` label was not checked. |
| VS Code | 1.145.2; `files.eol` set to LF in user settings |
| WSL | 3.0.5.0, kernel 6.18.58.1-1; `.wslconfig` caps memory at 3 GB, 4 processors, 2 GB swap |
| Docker Desktop | 4.99.0, engine 29.9.3, WSL 2 backend; `hello-world` ran; engine memory about 2.84 GiB, so the cap works. Re-checked 2026-11-13 after the owner signed in: engine 29.9.3 reachable, memory 3051933696 bytes. |
| Memory observations | Free RAM was about 0.7 to 0.9 GB with Firefox open and 2.1 GB with it closed. The Docker VM (`vmmemWSL`) used 223 MB with an idle database and the container 65 MB. Close Firefox before heavy Docker work. |
| PostgreSQL | **18.6 in a container** (`halo-db`, image `postgis/postgis:18-3.6`, digest `sha256:4a43e3c3e5d55b9208240fc71db543b79c638766280c625a425bd0a2390989c4`), data in volume `halo_halo_pgdata`. Published on `127.0.0.1:5432` only (Docker port record, and a refused connection to the Wi-Fi address). Clean baseline verified 2026-11-15: extension `plpgsql` only, no PostGIS or tiger objects; PostGIS 3.6.4 binaries present but not enabled. Start with `docker compose up -d`, stop with `docker compose stop`. |

## Repository

- Location: `C:\Dev\halo` (deliberately outside OneDrive, no spaces in the path)
- Remote: `origin` at `https://github.com/ThembinkosiMadiba/halo.git`, **private**. Make it public only after a pre-publication review (secrets, personal data, licence).
- Commit author: Thembinkosi Madiba, using the personal Gmail address configured globally in Git. This address will be permanent in public history.
- History: see `git log --oneline`. Some early commits have misleading messages (an empty `PROJECT_STATUS.md` was committed first, and one commit message promises a document it did not contain). Later commits say so; history was deliberately not rewritten.
- `frontend/` is intentionally not created yet; the Vite scaffold tool will create it.
- Database files: `docker-compose.yml`, `infrastructure/docker/initdb/` (replaces the image first-run script), `scripts/verify-database-baseline.ps1` (read-only baseline check) and `scripts/reset-database.ps1` (guarded, destructive). `.env` is git-ignored; `.env.example` is the template.

## Documents written

| Document | Path | State |
|---|---|---|
| Project overview | `README.md` | Committed |
| Scope, boundaries and data classification | `docs/governance/scope-and-boundaries.md` | Draft v0.1 |
| Threat model (v0.1, local deployment) | `docs/security/threat-model.md` | Draft v0.1 |
| System architecture | `docs/architecture/system-architecture.md` | Draft v0.1 |
| Initial database design | `docs/architecture/database-design.md` | Draft v0.1 |
| Data-source register | `docs/research/data-source-register.md` | Draft v0.1 |
| Decision register | `docs/architecture/decision-register.md` | Draft v0.1 |
| Product requirements | `docs/governance/product-requirements.md` | Draft v0.1 |
| Development plan | `docs/governance/development-plan.md` | Draft v0.1 |

## Decisions made

1. Python 3.14 for HALO's virtual environment, not 3.15.
2. Modular monolith; Docker is a convenience, not a requirement for core development.
3. GitHub repository is private until a pre-publication review.
4. LF line endings everywhere, except `.bat`, `.cmd` and `.ps1`.
5. Files are created in VS Code. Before `git add`, check the file is saved (no dot on its tab) and its path in `git status` is correct.
6. Confirmed by the owner (2026-11-13): all seven roles are modelled; only administrator, investigator and read-only are enabled in v0.1; user-submitted reports are deferred to Phase 5. Interpretation of "administrator" as organisation administrator is proposed in the architecture document and awaits confirmation.
7. Confirmed by the owner (2026-11-14): use the phonenumberslite build for v0.1; carrier and geocoding enrichment are deferred until reliable, authoritative, legally usable sources exist. See decision register DEC-008.
8. Owner decision 2026-11-15: replace the image first-run script so the database starts clean; extensions are enabled only by version-controlled migrations (DEC-010).
9. Database image `postgis/postgis:18-3.6`, PostgreSQL 18.6, digest recorded (DEC-009). The Compose file uses the tag; the digest is recorded and not enforced.

## Open items

- [ ] Docker Desktop: the owner reports having signed in. Whether sign-in is mandatory is not verified, so documentation must not claim "no account required". This is separate from Docker's runtime state, which was verified on 2026-11-11 and is re-checked at each environment assessment.
- [ ] Software licence for HALO not chosen.
- [ ] Threat model open questions now have proposed defaults in the architecture document (sessions, evidence storage, MFA), awaiting owner review.
- [ ] Development plan open decisions (section 9 of `development-plan.md`) await owner review: the vertical-slice ordering, the v0.1 risk rules and thresholds, feature branches, and when multi-factor authentication arrives.
- [ ] Product requirements open decisions (section 8 of `product-requirements.md`) await owner review, including whether to add a "Not assessed: insufficient information" risk result.
- [ ] Database design open decisions (section 10 of `database-design.md`) await owner review.
- [ ] At install time: verify the phonenumberslite licence and version, and that parsing, validity, region and number type work without the carrier and geocoding data.
- [x] Database login rules tested 2026-11-15: from another container on the Compose network, a wrong password was refused and the correct one accepted (threat T20). The database log names the rule scram-sha-256.
- [ ] M1 exit criterion "connection verified from Windows" is only partly met: a TCP connection to 127.0.0.1:5432 succeeded, but no SQL login through the published port has been tested.
- [ ] The database container was found stopped on 2026-11-14 at 22:40 UTC after a clean shutdown (exit 0, not out of memory). The cause is unknown. Available memory was about 900 MB when it was restarted, so close Firefox before Docker work.
- [ ] How the migration that enables PostGIS gets the privilege it needs while the application account stays non-superuser (T19).
- [ ] `.gitignore` lost its trailing newline on 2026-11-14 for an unknown reason and was restored. If it recurs, check VS Code settings.
- [ ] Licences of the database image contents not verified.
- [ ] South African legal questions are listed in the scope document but not yet researched (POPIA, RICA, Cybercrimes Act, Electronic Communications Act, ICASA numbering rules).
- [ ] The legacy `py.exe` launcher shadows the new one on PATH. Harmless; use `pymanager` and `python3.14` explicitly.
- [ ] `.vscode/` is git-ignored, so editor settings are not shared. Add an `.editorconfig` later.
- [ ] Enable the VS Code `files.insertFinalNewline` setting.

## Next steps

1. Answer the open decisions that block later milestones: feature branches (M2); MFA timing, email uniqueness, one role per user, the seeded system organisation, keeping submitted_text, trigger-based append-only protection (M3).
2. M2: create the backend virtual environment with Python 3.14 and install pinned dependencies, checking each licence at install.
3. Build the backend skeleton and health endpoint with tests, including a database connection test from Windows through the published port.
