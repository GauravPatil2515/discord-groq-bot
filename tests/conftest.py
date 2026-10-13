import os

import pytest


@pytest.fixture(autouse=True)
def clean_env():
    """Ensure tests run with predictable environment variables."""
    old_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(old_env)
