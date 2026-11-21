# HALO: Dependency Register (backend, M2)

**Status:** Draft v0.1
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-21

Every dependency is recorded with its version, declared licence and role. Licences below are what each package **declares in its own metadata**, read from the installed packages on 2026-11-15. They are not a legal review. Packages are installed with `--only-binary=:all:` so no third-party build script runs during installation.

## Environment

- Python 3.14.10, virtual environment at `backend/.venv` (git-ignored).
- Install: `backend\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r backend\requirements.txt`
- 28 packages pinned to exact versions in `backend/requirements.txt`.
- Verified: `pip check` reports no broken requirements; the installed set equals the file; every module imports. A rebuild from the file used pip's cache, so it was not a fresh network resolution.
- Smart App Control is enforcing on the development machine. Only two packages here contain compiled extensions (`psycopg-binary` and `pydantic-core`), and both normally load, but Smart App Control blocked the unsigned libpq library bundled in `psycopg-binary` once on 2026-11-19 (DEC-014). See also DEC-012.
- Linux: on 2026-11-21 GitHub Actions installed all 28 pinned packages with `--only-binary=:all:` on a Linux runner using Python 3.14.10, so prebuilt Linux wheels exist for each. Windows wheels were verified earlier on the development machine.

## Packages

| Package | Version | Declared licence | Compiled | Role |
|---|---|---|---|---|
| fastapi | 0.163.0 | MIT | No | Direct: API framework |
| uvicorn | 0.54.0 | BSD-3-Clause | No | Direct: server |
| pydantic-settings | 2.16.3 | MIT | No | Direct: configuration from environment variables |
| psycopg | 3.3.9 | LGPL-3.0-only | No | Direct: PostgreSQL driver |
| psycopg-binary | 3.3.9 | LGPL-3.0-only | Yes | Direct (extra of psycopg): prebuilt driver library |
| pytest | 9.2.0 | MIT | No | Direct: tests |
| httpx | 0.28.1 | BSD-3-Clause | No | Direct: test client |
| starlette | 1.10.0 | BSD-3-Clause | No | Dependency of fastapi |
| anyio | 4.16.0 | MIT | No | Dependency of fastapi |
| pydantic | 2.14.3 | MIT | No | Dependency of fastapi |
| pydantic-core | 2.50.4 | MIT | Yes | Dependency of pydantic |
| annotated-types | 0.8.0 | MIT | No | Dependency of pydantic |
| typing-extensions | 4.16.0 | PSF-2.0 | No | Dependency of fastapi |
| typing-inspection | 0.4.5 | MIT | No | Dependency of fastapi |
| annotated-doc | 0.0.6 | MIT | No | Dependency of fastapi |
| opentelemetry-api | 1.45.2 | Apache-2.0 | No | Dependency of fastapi (required) |
| click | 8.5.1 | BSD-3-Clause | No | Dependency of uvicorn |
| h11 | 0.16.0 | MIT | No | Dependency of uvicorn |
| python-dotenv | 1.2.4 | BSD-3-Clause | No | Dependency of pydantic-settings |
| tzdata | 2026.6 | Apache-2.0 | No | Dependency of psycopg |
| colorama | 0.4.6 | BSD License | No | Dependency of pytest |
| iniconfig | 2.3.1 | MIT | No | Dependency of pytest |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause | No | Dependency of pytest |
| pluggy | 1.7.0 | MIT | No | Dependency of pytest |
| Pygments | 2.21.0 | BSD-2-Clause | No | Dependency of pytest |
| certifi | 2026.10.23 | MPL-2.0 | No | Dependency of httpx |
| httpcore | 1.0.9 | BSD-3-Clause | No | Dependency of httpx |
| idna | 3.20 | BSD-3-Clause | No | Dependency of httpx |

## Licence notes

- **psycopg and psycopg-binary: LGPL-3.0-only (declared).** Using an unmodified LGPL library is normally allowed. Obligations may apply if HALO is ever distributed bundled with it. The binary wheel includes C libraries whose own licences were not checked. Flag for review by a qualified person, with the HALO software licence decision.
- **certifi: MPL-2.0 (declared).** A file-level licence. No obligation is expected from using the package unmodified. Not reviewed legally.

## Data flow and accounts

- Installing contacts PyPI. No account is needed.
- FastAPI requires `opentelemetry-api` unconditionally. Its SDK and exporter packages are only optional extras and are **not installed**. `opentelemetry-api` itself requires only `typing-extensions`. That strongly suggests it cannot send telemetry on its own, but runtime network behaviour has not been tested.
- No other runtime package is known to make network calls. This has not been tested.

## Planned for M3 and later (not installed in the project environment)

| Package | Tested version | Result in a throwaway environment on 2026-11-15 | Licence checked? |
|---|---|---|---|
| SQLAlchemy | 2.0.57 (a pin of `>=2.0,<2.1` is **proposed**) | Imports and runs a query. Windows blocked its compiled extension and the library fell back to pure Python | Not read for this version |
| argon2-cffi (with argon2-cffi-bindings, cffi) | 25.1.0 | Loads; produced an argon2id hash | Not read |
| MarkupSafe, greenlet | 3.0.4, 3.5.6 | Load | Not read |
| phonenumberslite | 9.0.43 | Resolved in a dry run as a pure-Python wheel; not yet installed or run | Not read |
| Alembic | 1.20.1 | Resolved in a dry run only, alongside SQLAlchemy 2.1; **not tested with SQLAlchemy 2.0.57** | Not read |

Each gets its licence read and its behaviour tested on its own branch before use.

## Database driver candidate (tested 2026-11-21, not installed in the project environment)

| Package | Version | Declared licence | Compiled |
|---|---|---|---|
| pg8000 | 1.31.6 | BSD 3-Clause License | No |
| scramp | 1.5.0 | MIT-0 | No |
| asn1crypto | 1.5.1 | MIT | No |
| python-dateutil | 4.0.0 | BSD-3-Clause | No |
| SQLAlchemy | 2.0.58 | MIT | Optional extensions (blocked by Smart App Control, falls back to pure Python) |
| greenlet | 3.5.6 | MIT AND PSF-2.0 | Yes (loaded in the test; installed as a dependency of SQLAlchemy 2.0) |

Result: direct and SQLAlchemy connections ran `select 1` against PostgreSQL 18.6, and a wrong password was refused. Proposed in DEC-016. Licences are as declared by the packages and have not been reviewed legally.

## Not done

- No hash pinning (`--require-hashes`). Exact version pinning limits but does not remove supply-chain risk.
- Release ages were not checked, so a very recently published release cannot be ruled out.
- pip itself has an unaddressed upgrade notice (26.2.2 to 26.3).
- No automated vulnerability scan yet.
- pytest reports a `StarletteDeprecationWarning`: Starlette's test client prefers `httpx2` over `httpx`. `httpx2` is an optional extra of FastAPI and is not installed. It needs its licence read and a Smart App Control test before use. The warning is not an error with the pinned versions.
