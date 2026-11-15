import pytest
from pydantic import ValidationError

from app.core.config import Settings

SECRET = "s3cret-value-for-tests-only"


def test_defaults_are_safe():
    settings = Settings(_env_file=None)
    assert settings.environment == "production"
    assert settings.api_host == "127.0.0.1"
    assert settings.docs_enabled is False
    assert settings.db_password is None


def test_non_loopback_api_host_is_rejected():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, api_host="0.0.0.0")


def test_loopback_hosts_are_accepted():
    for host in ("127.0.0.1", "::1", "localhost"):
        assert Settings(_env_file=None, api_host=host).api_host == host


def test_privileged_port_is_rejected():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, api_port=80)


def test_password_never_appears_in_text_forms():
    settings = Settings(_env_file=None, db_password=SECRET)
    assert SECRET not in repr(settings)
    assert SECRET not in str(settings)
    assert SECRET not in str(settings.model_dump())
    assert SECRET not in settings.model_dump_json()
    assert settings.db_password.get_secret_value() == SECRET


def test_environment_variable_enables_docs(monkeypatch):
    monkeypatch.setenv("HALO_ENVIRONMENT", "development")
    assert Settings(_env_file=None).docs_enabled is True
