# Contributing to HALO

This file describes how changes are made to HALO. HALO is currently a one-developer project, and the same rules apply to every change, including the owner's.

Status: draft v0.1, accepted by the owner on 2026-11-15 (decision DEC-011 in `docs/architecture/decision-register.md`).

## Principles

- `main` stays stable. It holds only work that has been tested and verified.
- Work happens on short-lived branches, one task per branch.
- History on `main` is never rewritten, and `main` is never force-pushed.
- Security comes before speed: no secrets, no real data, no unreviewed dependencies.

## What may go directly to `main`

Documentation-only changes:

- files under `docs/`
- `README.md`, `CONTRIBUTING.md` and `PROJECT_STATUS.md`

Everything else needs a branch, including code, tests, scripts, `docker-compose.yml`, `.gitignore`, `.gitattributes`, dependency files and CI configuration.

If a change mixes documentation with anything else, it goes on a branch.

## Branch workflow

Branch names use a prefix and a short description: `feat/phone-parsing`, `fix/login-throttle`, `test/audit-append-only`, `chore/backend-environment`, `docs/` for larger documentation work.

1. Make sure `main` is clean and current: `git switch main`, `git pull`, `git status`.
2. Create the branch: `git switch -c feat/short-topic`.
3. Work in small commits with the existing prefixes: `feat:`, `fix:`, `test:`, `docs:`, `chore:`.
4. Before every `git add`, check the file is saved and its path in `git status` is the expected one.
5. Run the verification gate below.
6. Merge into `main` (see Merge method), push, and delete the branch.

Keep branches short. A branch that lives for a long time is a sign that the task was too large, and it should be split.

## Verification gate before merging

A branch is merged only when all of these hold:

- The relevant automated tests pass. Until the test suite exists, the verification checks for that task have been run and their output recorded.
- Invalid-input and access-control cases are covered where relevant.
- Manual verification is recorded.
- Documentation and `PROJECT_STATUS.md` are updated.
- No secrets or real data are in the change. `.env` is never staged. A scan for the database password has been run.
- Remaining issues are listed.
- Dependencies added by the branch have had their licence, account requirement and data flow checked and recorded.

## Merge method (Proposed)

Merge locally with `git merge --no-ff feat/short-topic`, then `git push`. This keeps each task visible as one unit in the history. Revisit when automated checks run on GitHub, at which point pull requests become worth using. Not yet decided.

## If something broken reaches `main`

Do not rewrite history. Use `git revert <commit>` on a new branch, verify, and merge. Record what happened in `PROJECT_STATUS.md`.

## Not yet verified

Whether GitHub branch protection is available for this private repository on the current plan has not been checked. Nothing here relies on it.
