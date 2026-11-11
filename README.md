# HALO

HALO is an independently developed, open-source research project to build a modular platform for telecommunications-related fraud analysis and digital intelligence, with an initial focus on South Africa.

> **Status: early development (pre-alpha).** No application code exists yet. This repository currently contains project scaffolding only. Nothing here should be used for real investigations.

## Goals

- Analyse phone numbers using maintained numbering metadata, and report clearly what can and cannot be determined from a number alone.
- Correlate lawfully sourced, publicly available indicators to support fraud analysis.
- Provide explainable, rule-based risk assessments that always show their reasoning.
- Support investigation workflows with provenance, audit trails and evidence integrity.
- Run locally with a zero-cost core: no paid APIs, subscriptions or mandatory cloud services.

## Principles

- **Explainability.** Every result carries its source, timestamp, confidence and limitations. Assumptions are never presented as facts.
- **Human oversight.** Risk classifications are prioritisation aids, not findings of criminality. Consequential conclusions require human review.
- **Security by design.** Role-based access, organisation-level data separation and audit logging are built in from the start.
- **Privacy by design.** Data minimisation, retention controls and synthetic data for development and demonstrations.
- **Simplicity first.** A modular monolith, with complexity added only when there is a real engineering reason.

## What HALO will not do

- Access telecom systems or confidential subscriber records without authority.
- Intercept communications, track phones covertly or perform unauthorised cellular triangulation.
- Determine a device's physical location from a phone number alone.
- Publicly accuse individuals based on automated scores.
- Bypass authentication or access controls to collect data.

## Planned technology

Python (FastAPI, SQLAlchemy, Alembic, Pytest), PostgreSQL with PostGIS, React with TypeScript, and Docker. These are proposals and may change as the project develops.

## Roadmap

Development proceeds in phases: environment and foundation, phone-number intelligence, intelligence data framework, fraud analysis, geospatial and relationship analysis, investigation workspace, security and quality assurance, then deployment and publication. See `PROJECT_STATUS.md` for current progress.

## Legal notice

HALO is being developed with South African law in mind, including POPIA, RICA and the Cybercrimes Act. Nothing in this repository is legal advice. Any real-world deployment requires review by a qualified South African legal professional.

## Licence

To be decided before the first public release.