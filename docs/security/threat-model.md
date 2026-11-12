# HALO: Threat Model (v0.1, local deployment)

**Status:** Draft v0.1 (Phase 0)
**Owner:** Thembinkosi Madiba
**Last updated:** 2026-11-12

This model covers HALO v0.1 only: a single organisation on one Windows machine, reachable from that machine only. It lists planned mitigations. **None are implemented yet**, and none should be described as implemented until tested. Cloud deployment, external connectors and institutional integrations need their own model before they are built.

## 1. Assets

| ID | Asset | Why it matters |
|---|---|---|
| A1 | Phone numbers and analysis records | Likely personal information; exposure can harm individuals |
| A2 | Evidence files and their hashes | Integrity is what makes evidence credible |
| A3 | Investigation notes and relationships | Sensitive; may contain unproven allegations |
| A4 | Credentials, session tokens, secrets | Compromise gives access to everything else |
| A5 | Audit log | Accountability depends on it being complete and unaltered |
| A6 | Risk assessments | A wrong or leaked classification can damage a person or number's reputation |
| A7 | Source repository and dependencies | Compromise could insert malicious code or leak secrets |

## 2. Actors

| Actor | Description |
|---|---|
| Legitimate user | Authorised user acting within their role |
| Curious or malicious insider | Authorised user reaching beyond their role or organisation |
| Local-network attacker | Another device on the same network |
| Malware on the workstation | Hostile software running as the user |
| Misuser | Someone using HALO to harass, stalk or defame a person |
| Supply-chain attacker | Compromises a dependency or container image |
| The developer | Mistakes such as committing a secret or exposing a port |

## 3. Trust boundaries

1. Browser to API
2. API to database
3. API to file storage (evidence)
4. HALO to the internet (none in v0.1)
5. Developer machine to GitHub

## 4. Threats and planned mitigations

| ID | Threat | Category | Planned mitigation | Planned verification |
|---|---|---|---|---|
| T1 | A user reads another organisation's data by changing an ID | Information disclosure (broken access control, IDOR) | Server-side organisation filter on every query; no trust in client-supplied IDs | Automated cross-organisation access tests |
| T2 | A user performs an action above their role | Elevation of privilege | Role checks enforced in the API for every endpoint | Per-role endpoint test matrix |
| T3 | Password guessing or credential stuffing | Spoofing | Argon2id hashing; login throttling; generic error messages | Rate-limit and error-message tests |
| T4 | Stolen or reused session token | Spoofing | Short-lived sessions; secure cookie flags; logout invalidates server-side | Session tests |
| T5 | SQL injection | Tampering | Parameterised queries through the ORM; no string-built SQL | Injection tests; code review |
| T6 | Cross-site scripting through stored notes or numbers | Tampering | Output encoding; strict content-security policy | XSS tests |
| T7 | Cross-site request forgery | Tampering | Token or same-site cookie protection | CSRF tests |
| T8 | Malicious file upload as "evidence" | Tampering, denial of service | Type and size limits; stored outside the web root; never executed; hashed on receipt | Upload tests |
| T9 | Evidence altered after the fact | Tampering, repudiation | SHA-256 at ingest; append-only change history; no silent edits | Integrity tests |
| T10 | Audit log altered or deleted | Repudiation | Append-only table; application account has no update or delete permission | Permission tests |
| T11 | Secrets or real data committed to Git | Information disclosure | `.gitignore` (in place); `.env.example` only; secret scanning before publication | Repository scan before public release |
| T12 | Database or API exposed beyond this machine | Information disclosure | Bind to `127.0.0.1` only; no published ports except local; no default passwords | Port and bind checks |
| T13 | Sensitive data in logs or error messages | Information disclosure | Redaction; generic errors to clients; no numbers or tokens in logs | Log inspection tests |
| T14 | Vulnerable dependency or tampered container image | Tampering | Pinned versions; dependency scanning; official images only | Automated dependency scan |
| T15 | Backup or database dump leaks data | Information disclosure | Dumps git-ignored; documented handling; encrypted at rest where practical | Backup and restore test |
| T16 | HALO used to harass or defame a person or number | Misuse | Risk labels are prioritisation aids, not criminal findings; human review before any external use; audit trail; no automatic dissemination | Review of wording and workflow |
| T17 | Misleading output treated as fact | Misuse | Every result carries class, source, timestamp, confidence and limitations; "Not available" instead of guesses | Output review tests |
| T18 | Over-collection of personal data | Misuse, privacy | Data minimisation; retention rules; synthetic data by default | Retention tests |

## 5. Assumptions and out of scope

- The operating system and hardware are trusted. A fully compromised Windows account defeats most local mitigations, and HALO cannot fix that.
- Physical access to the machine is out of scope.
- v0.1 has no external network connectors. Each future connector needs its own entry here.
- Encryption in transit matters little for a single-machine loopback deployment, but it becomes mandatory before any network or cloud deployment.

## 6. Open items

- [ ] Decide how evidence files are stored (filesystem with hashes recorded in the database, or database storage).
- [ ] Decide the session mechanism (server-side sessions or signed tokens).
- [ ] Decide whether multi-factor authentication is in v0.1 or a later release.
- [ ] Extend this model before Phase 4 (external sources) and before any cloud deployment.