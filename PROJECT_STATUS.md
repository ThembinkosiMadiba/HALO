# HALO: Project Status

Resume point for development sessions. Update at the end of every milestone.
Only verified facts are recorded as facts; everything else is marked as open.

**Last updated:** 2026-11-11
**Current phase:** Phase 1 (Windows development environment), nearly complete
**Next milestone:** Phase 0 documents, then database setup and the backend foundation

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
- Remote: none yet. The GitHub repository will be created as **private** and made public only after a pre-publication review.
- Commit author: Thembinkosi Madiba, using the personal Gmail address configured globally in Git. This address will be permanent in public history.

| Commit | Purpose |
|---|---|
| f581a4a | `.gitignore` with secret and data protections |
| 0d39f33 | Folder scaffold (26 `.gitkeep` placeholders) |
| 423bdb0 | `.gitattributes` (LF line endings) |
| 9f4e9ea | `README.md` |

`frontend/` is intentionally not created yet; the Vite scaffold tool will create it.

## Decisions made

1. Python 3.14 for HALO's virtual environment, not 3.15.
2. Modular monolith; Docker is a convenience, not a requirement for core development.
3. GitHub repository starts private.
4. LF line endings everywhere, except `.bat`, `.cmd` and `.ps1`.
5. Files are created in VS Code, not PowerShell here-strings.

## Open items

- [ ] Whether Docker Desktop required sign-in is unknown. Needed before documentation claims "no account required".
- [ ] Software licence for HALO not chosen.
- [ ] The legacy `py.exe` launcher shadows the new one on PATH. Harmless; use `pymanager` and `python3.14` explicitly.
- [ ] The `.vscode/` folder is git-ignored, so editor settings are not shared. Add an `.editorconfig` later.
- [ ] No Phase 0 documents exist yet: product requirements, architecture, data-source register, initial database design, threat model, development plan. These come before substantial application code.
- [ ] South African legal review items are flagged, not yet researched (POPIA, RICA, Cybercrimes Act, Electronic Communications Act, ICASA numbering rules).

## Next steps

1. Write the Phase 0 documents, starting with scope and the threat model.
2. Create the private GitHub repository and push.
3. Start PostgreSQL with PostGIS via Docker Compose and verify it.
4. Create the backend virtual environment with Python 3.14.
5. Start Phase 2: FastAPI skeleton and health-check endpoint.