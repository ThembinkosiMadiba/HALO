"""Logging setup.

SecretRedactionFilter replaces configured secret values in log MESSAGES with a marker.
Limit: it does not look inside exception tracebacks. Never log secrets on purpose.
"""
import logging
from typing import TextIO

from app.core.config import Settings

LOGGER_NAME = "halo"
REDACTED = "[REDACTED]"


class SecretRedactionFilter(logging.Filter):
    def __init__(self, secrets: list[str]) -> None:
        super().__init__()
        self._secrets = [secret for secret in secrets if secret]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        redacted = message
        for secret in self._secrets:
            redacted = redacted.replace(secret, REDACTED)
        if redacted != message:
            record.msg = redacted
            record.args = None
        return True


def configure_logging(settings: Settings, stream: TextIO | None = None) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    secrets: list[str] = []
    if settings.db_password is not None:
        secrets.append(settings.db_password.get_secret_value())
    handler.addFilter(SecretRedactionFilter(secrets))

    logger.addHandler(handler)
    logger.setLevel(settings.log_level)
    logger.propagate = False
    return logger
