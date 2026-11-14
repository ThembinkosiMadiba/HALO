# HALO: Data-Source Register (v0.1)

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-14

Every source HALO uses must be listed here **before** it is used. "Verified" means checked by reading its documentation or terms; "Not verified" means it has not been. Nothing in this register is legal advice.

## 1. Approval rules

A source may be approved for use only when its entry records: what it is, where it comes from, its licence or terms of use, whether it contains personal data, how it is retrieved, how reliable it is, and how long data from it is kept. Each external connector (Phase 4) also needs an entry in the threat model.

Not permitted, whatever the source:

- Anything behind authentication that the owner has no right to use, or private accounts and groups.
- Confidential subscriber, operator, IMEI or law-enforcement data without documented legal authority.
- Bulk collection of personal information "because it is public".
- Content obtained by bypassing access controls, paywalls or rate limits.

## 2. Sources approved for v0.1

| ID | Source | Type | Provides | Licence and terms | Personal data | Retrieval | Reliability | Retention |
|---|---|---|---|---|---|---|---|---|
| DS-001 | `phonenumberslite` Python library (lite build of the port of Google libphonenumber) | Software library with bundled core metadata | Parsing, formatting, possible and valid checks, region, number type. **Excludes** carrier, geocoding and timezone data. | Apache 2.0 per PyPI listings. **Re-verify the exact licence and any NOTICE file at install time.** | None | Installed once; works offline | High for format and structure; **not** proof a number is assigned, active or currently on a given network | Library version recorded in every analysis |
| DS-002 | `halo_rules` | Internal | Rule-based findings and risk reasoning | HALO's own code | Derived from stored data | Internal | Only as good as the documented rules; versioned | Follows the records it describes |
| DS-003 | `manual_entry` | Internal | Analyst-entered observations | Entered by an authorised user | Possible | User input | Unconfirmed until reviewed | Follows the investigation |
| DS-004 | Synthetic data generator | Internal | Artificial numbers, reports and events for development and demos | HALO's own code | None, by design | Generated locally | Not real; always labelled synthetic | Disposable |

## 3. Reference sources (read by people, not ingested by software)

| ID | Source | Why it matters | Status |
|---|---|---|---|
| DS-010 | ICASA Numbering Plan Regulations, 2016 (Government Gazette notice 370, 24 March 2016) and its amendments | Defines how South African numbers are structured and allocated. The Fourth Amendment Regulations, 2025 have been published. | **Contents not read; licence and terms not verified.** To read before HALO claims anything about South African number ranges. |
| DS-011 | ICASA Number Portability Regulations | Explains why a prefix does not identify the current operator | Contents not read; terms not verified |
| DS-012 | ICASA numbering pages (`icasa.org.za`) | Official statements on the numbering resource | Terms not verified |

Rule: until DS-010 and DS-011 have been read, HALO's South African output states only what DS-001 returns, and **does not** name an operator or a number range's owner.

## 4. Candidate categories (not evaluated, not approved)

These are research areas for Phase 4. They are categories, not named sources. Each needs its own register entry, with terms checked, before use.

| Category | Open questions |
|---|---|
| Public scam and fraud warnings from South African organisations | Who publishes them, in what form, under what terms, and do they name individuals? |
| Public cybersecurity advisories | Licence, and whether indicators are included |
| Public threat-intelligence feeds (domains, URLs, IPs) | Licence, update rate, reliability, whether commercial use is restricted |
| Business registers and public contact information | Lawful basis for collection under POPIA, and whether retention is appropriate |
| Open datasets on telecommunications | Licence, provenance, freshness |

## 5. Requirements for every future connector

- Source identification, reference or URL, and retrieval timestamp.
- Provenance and reliability class recorded with each result.
- Licence and usage restrictions recorded and respected.
- Error handling, with no silent failures.
- A rate limit and an identifying request header.
- Data-retention rule, and a way to delete a source's data.
- Respect for `robots.txt` and site terms.
- An entry in this register and in the threat model **before** any code is written.

## 6. Verification still owed

- [ ] Read DS-010 and DS-011 (and the Fourth Amendment) before describing South African number ranges.
- [ ] Check ICASA's terms of use for its published numbering information.
- [ ] Re-verify the `phonenumberslite` licence, NOTICE file and installed version at install time, and that parsing, validity, region and number type work without the carrier and geocoding data.
- [ ] Deferred: confirm what carrier metadata represents (likely the original allocation, not the current operator) before carrier enrichment is ever considered. Not needed for v0.1 because the lite build excludes it.
- [x] Decided 2026-11-14: use the lite build for v0.1 (decision DEC-008 in `docs/architecture/decision-register.md`).

## 7. Decisions

- [x] Lite build of the phone-number library for v0.1 (2026-11-14, owner decision, DEC-008).
- [x] Reference sources stay in this register for now and are revisited in Phase 4 (2026-11-14, owner delegated this to the recommended approach).
