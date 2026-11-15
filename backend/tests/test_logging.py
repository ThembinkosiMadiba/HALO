import io
import logging

from app.core.config import Settings
from app.core.logging_config import REDACTED, SecretRedactionFilter, configure_logging

SECRET = "pw-very-secret-for-tests-1"


def make_record(message: str, *args) -> logging.LogRecord:
    return logging.LogRecord("halo", logging.INFO, __file__, 1, message, args, None)


def test_filter_redacts_secret_in_message():
    record = make_record("connecting with %s", SECRET)
    SecretRedactionFilter([SECRET]).filter(record)
    assert SECRET not in record.getMessage()
    assert REDACTED in record.getMessage()


def test_filter_ignores_empty_secrets_and_leaves_other_text():
    record = make_record("nothing sensitive here")
    SecretRedactionFilter([""]).filter(record)
    assert record.getMessage() == "nothing sensitive here"


def test_configured_logger_redacts_the_database_password():
    stream = io.StringIO()
    configure_logging(Settings(_env_file=None, db_password=SECRET, log_level="INFO"), stream=stream)
    logging.getLogger("halo").info("password is %s", SECRET)
    output = stream.getvalue()
    assert SECRET not in output
    assert REDACTED in output
