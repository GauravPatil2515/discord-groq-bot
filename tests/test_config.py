import os

import pytest


def get_secret(name: str) -> str | None:
    val = os.getenv(name)
    if not val:
        try:
            from google.colab import userdata

            val = userdata.get(name)
        except Exception:
            pass
    return val


def test_get_secret_from_env():
    os.environ["DISCORD_BOT_TOKEN"] = "test_token_123"
    assert get_secret("DISCORD_BOT_TOKEN") == "test_token_123"


def test_get_secret_missing():
    os.environ.pop("NON_EXISTENT_KEY", None)
    assert get_secret("NON_EXISTENT_KEY") is None


def test_guild_id_parsing():
    raw_id = "987654321012345678"
    assert int(raw_id) == 987654321012345678


def test_invalid_guild_id_parsing():
    with pytest.raises(ValueError):
        int("invalid_alphanumeric_id")
