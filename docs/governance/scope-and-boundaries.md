# HALO: Scope, Boundaries and Data Classification

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-12

This document defines what HALO v0.1 includes, who may use it, what it must never do, and how data is classified. Items marked **Proposed** are design suggestions awaiting the owner's decision. Nothing in this document is legal advice.

## 1. Purpose

HALO is a research platform for telecommunications-related fraud analysis. v0.1 is deliberately narrow: analyse a phone number's numbering metadata, record it as an intelligence record, link it to an investigation, and show an explainable initial risk assessment.

## 2. HALO v0.1 scope

### In scope

- Run locally on Windows 11 and be reachable only from the local machine by default.
- Authenticate users securely.
- Analyse a single phone number using a maintained numbering library, with South African support.
- Show source, timestamp, confidence and limitations; show "Not available" instead of inventing data.
- Save an analysis as an intelligence record.
- Create an investigation, attach the record, and attach synthetic or authorised evidence with integrity hashes.
- Produce an explainable, rule-based initial risk assessment.
- Generate an investigation summary.
- Record an audit trail of significant actions.

### Out of scope for v0.1

- Bulk analysis, CSV import and external OSINT connectors (later phases).
- Machine learning of any kind.
- Maps, relationship graphs and device (IMEI) analysis (later phases).
- Cloud deployment and any external dissemination of results.
- Any real subscriber, network-operator or law-enforcement data.

## 3. Users and roles

HALO is designed for researchers, analysts, fraud teams, security organisations and authorised institutions. Permissions are enforced on the server, never only by hiding buttons.

| Role | Intended capability |
|---|---|
| Platform administrator | Manages the installation and organisations |
| Organisation administrator | Manages users and settings within one organisation |
| Investigator | Creates and works investigations |
| Intelligence analyst | Analyses indicators and records findings |
| Researcher | Works with synthetic and public data |
| Reviewer | Reviews findings before any consequential use |
| Read-only user | Views permitted records only |

**Proposed:** implement the database model for all seven roles from the start, but enable only administrator, investigator and read-only in v0.1. Organisation-level data separation is enforced from day one even though v0.1 has one organisation.

## 4. Prohibited activities

HALO must never be built or used to:

- Access telecom systems or confidential subscriber records without documented legal authority.
- Intercept communications, track devices covertly, or perform unauthorised cellular triangulation.
- Infer a device's physical location from a phone number alone.
- Access IMEI or operator databases without authorisation.
- Impersonate law enforcement, dox individuals, or "hack back".
- Bypass authentication or access controls, or scrape private accounts.
- Publicly accuse any person or number based solely on an automated score.

## 5. Information classes

Every result HALO stores must carry exactly one of these classes, plus provenance, timestamp and confidence.

| Class | Meaning |
|---|---|
| Verified | Confirmed against an authoritative source or by documented human review |
| Public | Obtained from a lawful public source, with the source recorded |
| User-submitted | Reported by a user and not independently confirmed |
| Analytical finding | Derived by a documented HALO rule from the data above |
| Estimate | An approximation, with its method and limits stated |
| Hypothesis | An analyst's unconfirmed proposal |
| Unavailable | Not obtainable; shown as "Not available" and never filled in |

Number validity is **not** proof that a subscriber exists or that a number is active. A number's prefix does **not** conclusively identify its current operator, because mobile number portability exists.

## 6. Data categories

| Category | Handling in development |
|---|---|
| Synthetic data | The default for all development, tests and public demonstrations |
| Public data | Only from sources recorded in the source register, with licence checked |
| User-submitted reports | Only with consent records and a stated purpose; **Proposed:** not enabled before Phase 5 |
| Institutional data | Not used until documented legal authority, a formal agreement and a security assessment exist |

Phone numbers are likely to count as personal information, and IMEIs are sensitive identifiers. Both require data minimisation, access control, retention limits and no exposure in logs or error messages. Real numbers must never be committed to the repository.

## 7. Risk classification

The initial scale is Low, Guarded, Elevated, High and Critical. These are prioritisation aids, not probabilities of criminality. Every classification must show the rules and evidence behind it. A human must review before any consequential conclusion or external dissemination.

## 8. Questions for a South African legal professional

These have **not** been researched yet. They are listed so none is forgotten.

- Whether and how the Protection of Personal Information Act (POPIA) applies to storing phone numbers and fraud reports, including lawful basis, purpose limitation, retention, and responsible-party obligations.
- Whether any planned function could engage the Regulation of Interception of Communications and Provision of Communication-related Information Act (RICA).
- Obligations and risks under the Cybercrimes Act, including reporting duties.
- Relevance of the Electronic Communications Act and ICASA numbering-plan rules, and the licence terms of ICASA's published numbering information.
- Conditions under which user-submitted fraud reports may be stored and shared.
- Requirements before any institutional or law-enforcement integration.

## 9. Open decisions

- [ ] Accept or change the **Proposed** role rollout in section 3.
- [ ] Accept or change the **Proposed** timing for user-submitted reports in section 6.
- [ ] Choose a software licence for HALO.