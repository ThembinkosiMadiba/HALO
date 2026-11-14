# HALO: Decision Register

**Status:** Draft v0.1
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-14

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