import os

import pytest


@pytest.fixture(autouse=True)
def clean_halo_environment(monkeypatch):
    """Tests must not depend on HALO_* variables from the developer's shell."""
    for key in list(os.environ):
        if key.startswith("HALO_"):
            monkeypatch.delenv(key, raising=False)
