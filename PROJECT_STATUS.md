# HALO: Project Status

Resume point for development sessions. Update at the end of every milestone.
Only verified facts are recorded as facts; everything else is marked as open.

**Last updated:** 2026-11-13
**Current phase:** Phase 0 (requirements and governance documents). The Phase 1 environment is complete except PostgreSQL.
**Next milestone:** Remaining Phase 0 documents, then PostgreSQL with PostGIS via Docker Compose, then the backend foundation

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
| Docker Desktop | 4.99.0, engine 29.9.3, WSL 2 backend; `hello-world` ran; engine memory about 2.84 GiB, so the cap works |
| PostgreSQL | **Not installed.** Plan: PostgreSQL with PostGIS in a Docker container, with a native install as fallback. |

## Repository

- Location: `C:\Dev\halo` (deliberately outside OneDrive, no spaces in the path)
- Remote: `origin` at `https://github.com/ThembinkosiMadiba/halo.git`, **private**. Make it public only after a pre-publication review (secrets, personal data, licence).
- Commit author: Thembinkosi Madiba, using the personal Gmail address configured globally in Git. This address will be permanent in public history.
- History: see `git log --oneline`. Some early commits have misleading messages (an empty `PROJECT_STATUS.md` was committed first, and one commit message promises a document it did not contain). Later commits say so; history was deliberately not rewritten.
- `frontend/` is intentionally not created yet; the Vite scaffold tool will create it.

## Documents written

| Document | Path | State |
|---|---|---|
| Project overview | `README.md` | Committed |
| Scope, boundaries and data classification | `docs/governance/scope-and-boundaries.md` | Draft v0.1 |
| Threat model (v0.1, local deployment) | `docs/security/threat-model.md` | Draft v0.1 |

## Decisions made

1. Python 3.14 for HALO's virtual environment, not 3.15.
2. Modular monolith; Docker is a convenience, not a requirement for core development.
3. GitHub repository is private until a pre-publication review.
4. LF line endings everywhere, except `.bat`, `.cmd` and `.ps1`.
5. Files are created in VS Code. Before `git add`, check the file is saved (no dot on its tab) and its path in `git status` is correct.
6. Working assumptions, not yet explicitly confirmed by the owner: model all seven roles in the database but enable only administrator, investigator and read-only in v0.1; user-submitted reports not before Phase 5.

## Open items

- [ ] Whether Docker Desktop required sign-in: **not verified**. Needed before documentation claims "no account required".
- [ ] Software licence for HALO not chosen.
- [ ] Owner to confirm or change the working assumptions in decision 6.
- [ ] Threat model open questions: evidence storage method, session mechanism, whether multi-factor authentication is in v0.1.
- [ ] Remaining Phase 0 documents: product requirements, system architecture, data-source register, initial database design, development plan.
- [ ] South African legal questions are listed in the scope document but not yet researched (POPIA, RICA, Cybercrimes Act, Electronic Communications Act, ICASA numbering rules).
- [ ] The legacy `py.exe` launcher shadows the new one on PATH. Harmless; use `pymanager` and `python3.14` explicitly.
- [ ] `.vscode/` is git-ignored, so editor settings are not shared. Add an `.editorconfig` later.
- [ ] Enable the VS Code `files.insertFinalNewline` setting.

## Next steps

1. Write the system architecture and initial database design documents.
2. Write the data-source register and the development plan.
3. Start PostgreSQL with PostGIS via Docker Compose and verify it.
4. Create the backend virtual environment with Python 3.14.
5. Start Phase 2: FastAPI skeleton and health-check endpoint.