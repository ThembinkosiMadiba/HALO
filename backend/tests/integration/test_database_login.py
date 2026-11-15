r"""Database login tests through the published port.

These tests need the local database container (docker compose up -d) and run only with:
    backend\.venv\Scripts\python.exe -m pytest backend -m integration

EXCEPTION to threat T19 (application code must never use the database owner account):
these tests are not application code. They use halo_owner, the only account that exists
until the first migration (milestone M3) creates the restricted halo_app account, and they
only open a connection and run SELECT. The password is read from .env and is never printed.
"""
from pathlib import Path

import psycopg
import pytest
from dotenv import dotenv_values

pytestmark = pytest.mark.integration

REPO_ROOT = Path(__file__).resolve().parents[3]


def _env() -> dict:
    values = dotenv_values(REPO_ROOT / ".env")
    if not values.get("POSTGRES_PASSWORD"):
        pytest.fail(".env with POSTGRES_PASSWORD is missing")
    return values


def _connect(password: str, user: str | None = None) -> psycopg.Connection:
    env = _env()
    return psycopg.connect(
        host="127.0.0.1",
        port=int(env.get("POSTGRES_PORT") or 5432),
        dbname=env.get("POSTGRES_DB") or "halo",
        user=user or env.get("POSTGRES_USER") or "halo_owner",
        password=password,
        connect_timeout=5,
    )


@pytest.fixture(scope="module", autouse=True)
def database_is_running():
    try:
        _connect(_env()["POSTGRES_PASSWORD"]).close()
    except psycopg.OperationalError as exc:
        # Only the exception type is reported, never its text.
        pytest.fail("Cannot connect with the .env credentials (" + type(exc).__name__ + "). Is the database running? Try: docker compose up -d")


def test_correct_password_is_accepted():
    with _connect(_env()["POSTGRES_PASSWORD"]) as conn:
        assert conn.execute("SELECT 1").fetchone() == (1,)
        version = conn.execute("SHOW server_version").fetchone()[0]
    assert version.startswith("18.")


def test_wrong_password_is_refused():
    with pytest.raises(psycopg.OperationalError) as info:
        _connect("this-is-not-the-password")
    assert "password authentication failed" in str(info.value)


def test_unknown_user_gets_the_same_refusal():
    with pytest.raises(psycopg.OperationalError) as info:
        _connect("this-is-not-the-password", user="no_such_user")
    assert "password authentication failed" in str(info.value)
