# HALO: Product Requirements (v0.1)

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-14

This document lists what HALO v0.1 must do, with a testable acceptance criterion for each requirement. It should be read with `scope-and-boundaries.md`, `system-architecture.md`, `database-design.md` and `threat-model.md`. Items marked **Proposed** await the owner's decision.

## 1. Goal

A user can open HALO locally, sign in, analyse a phone number, save the result, link it to an investigation, attach evidence, see an explainable initial risk assessment and generate an investigation summary, with every step attributed, audited and honest about its limits.

## 2. Functional requirements

| ID | Requirement | Acceptance criterion |
|---|---|---|
| FR-01 | HALO runs locally on Windows 11 and is reachable only from the same machine | The API and database accept connections only on `127.0.0.1`; a connection from another device on the network is refused |
| FR-02 | Users sign in with email and password and can sign out | Correct credentials give a session; wrong credentials and unknown users give the same generic error; sign-out invalidates the session on the server |
| FR-03 | Repeated failed sign-ins are throttled | After a set number of failures the account is delayed or locked temporarily, and the event is audited |
| FR-04 | An organisation administrator creates and deactivates users in their own organisation | Created users can sign in; deactivated users cannot; the administrator cannot see or change another organisation's users |
| FR-05 | A user analyses one phone number, in national or international format | South African examples such as `082 123 4567` and `+27821234567` (synthetic test values) normalise to the same E.164 value |
| FR-06 | The analysis shows submitted number, normalised number, country calling code, region, number type, validity result, metadata source and library version, timestamp, confidence and limitations | Every field is present; any field the lite library cannot supply shows "Not available" and is never guessed |
| FR-07 | Invalid or impossible input is rejected with a clear message and a stable error structure | Empty, non-numeric, too-long and malformed inputs return a validation error, never a server error and never an invented result |
| FR-08 | The interface never presents a valid number as proof that a subscriber exists, that the number is active, or that it is on a particular network | The wording is present on the result screen and is covered by a test |
| FR-09 | A user saves an analysis as an immutable intelligence record | The record is stored under the user's organisation; a repeat analysis creates a new row and never overwrites |
| FR-10 | A user creates an investigation and links a saved indicator to it | The investigation gets a reference unique within the organisation; the link is visible only to that organisation |
| FR-11 | A user adds observations to an investigation, each labelled with an information class | An edit creates a new observation and marks the old one superseded; history is retained |
| FR-12 | A user attaches evidence, either synthetic or appropriately authorised | The server records the SHA-256 on receipt and checks it again when the file is read; a tampered file is detected |
| FR-13 | Uploads are restricted by type and size and are never executed | Disallowed types and oversized files are rejected; files are stored under random names outside the web root |
| FR-14 | HALO produces a rule-based initial risk assessment that explains itself | The result lists each rule that fired and its supporting evidence, the ruleset version and the limitations; the wording says it prioritises attention and is not a probability of criminality |
| FR-15 | A risk assessment is a draft until a reviewer marks it reviewed | A reviewed status without a named reviewer and timestamp is rejected by the database |
| FR-16 | HALO generates an investigation summary on demand | The summary contains indicators, observations, evidence metadata with hashes, the assessment, provenance and limitations, and is labelled as a draft for human review |
| FR-17 | Significant actions are audited | Sign-ins, failures, role or user changes, investigation and evidence actions and summary generation each write an audit event with actor, time and outcome |
| FR-18 | Permissions and organisation separation are enforced by the server | A read-only user cannot create or change anything; a user from organisation A requesting an identifier from organisation B receives a not-found response |

## 3. Non-functional requirements

| ID | Requirement | Acceptance criterion |
|---|---|---|
| NFR-01 | Core analysis works offline and costs nothing to run | A number analysis succeeds with the network disabled; no paid service is called |
| NFR-02 | No sensitive data in logs or error responses | Inspection of logs and responses after failures finds no password, token or full phone number |
| NFR-03 | No secrets or real data in the repository | A scan of the repository history finds none, and `.env` is ignored |
| NFR-04 | The test suite is automated and covers each acceptance criterion in this document | Each criterion maps to at least one automated test, run on every push |
| NFR-05 | The system runs on the owner's machine (7.7 GB RAM) with Docker held to about 3 GB | HALO and its database run together without exhausting memory in normal use |
| NFR-06 | The interface is accessible and readable | Text meets accessible contrast; the main workflow works by keyboard |
| NFR-07 | Every dependency is free and its licence is recorded | The data-source register and architecture list each dependency's licence, checked at install time |
| NFR-08 | Numeric targets, such as the response time of a single analysis, are measured before they are promised | No performance figure appears in documentation without a recorded measurement |

## 4. Acceptance traceability to the project specification (section 20)

| v0.1 capability | Requirements |
|---|---|
| Open HALO locally | FR-01 |
| Access securely | FR-02, FR-03, FR-18 |
| Enter a phone number | FR-05 |
| Structured numbering analysis | FR-06, FR-07 |
| Source and limitations | FR-06, FR-08 |
| Save as an intelligence record | FR-09 |
| Associate with an investigation | FR-10, FR-11 |
| Attach evidence | FR-12, FR-13 |
| Explainable initial risk assessment | FR-14, FR-15 |
| Investigation summary | FR-16 |

## 5. Risk assessment in v0.1: an honest limit

v0.1 holds only numbering metadata and analyst notes. It has no independent reports and no external sources, so almost no rule will have enough evidence to fire. **Proposed:** when no rule has enough evidence, the result is **"Not assessed: insufficient information"**, not "Low". "Low" would suggest that checks were made and found nothing. The five classifications (Low, Guarded, Elevated, High, Critical) apply only when at least one documented rule produces a finding. The actual v0.1 rules are defined in the development plan and must each be justified, explainable and tested.

## 6. Deliberately not in v0.1

Bulk analysis and CSV import, external connectors and OSINT, carrier and geocoding data (excluded by DEC-008), device or IMEI analysis, maps, relationship graphs, user-submitted reports, machine learning, and cloud deployment. Multi-factor authentication is in the schema but is not required in v0.1.

## 7. Assumptions

- A single organisation and a handful of local users.
- Synthetic data only; no real subscriber or operator data.
- The owner is the sole developer and the first administrator.

## 8. Open decisions

- [ ] Accept the "Not assessed: insufficient information" result in section 5?
- [ ] Throttling thresholds for FR-03 (the number of failures and the lock duration).
- [ ] Uploaded file types and size limit for FR-13 (the architecture proposes PDF, PNG, JPEG, text and CSV, up to 10 MB).
- [ ] Whether the investigation summary needs an export format in v0.1, or whether on-screen display is enough.