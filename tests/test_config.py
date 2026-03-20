import os
import tempfile
from pathlib import Path

from quota_dash.config import load_config, AppConfig, ProviderConfig


SAMPLE_TOML = """\
[general]
polling_interval = 30
theme = "ghostty"
mode = "dashboard"

[providers.openai]
enabled = true
api_key_env = "OPENAI_API_KEY"
log_path = "~/.codex/"

[providers.anthropic]
enabled = false
api_key_env = "ANTHROPIC_API_KEY"
log_path = "~/.claude/"
"""


def test_load_config_from_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(SAMPLE_TOML)
        f.flush()
        config = load_config(Path(f.name))
    os.unlink(f.name)

    assert config.polling_interval == 30
    assert config.theme == "ghostty"
    assert config.mode == "dashboard"
    assert "openai" in config.providers
    assert config.providers["openai"].enabled is True
    assert config.providers["anthropic"].enabled is False


def test_load_config_defaults():
    config = load_config(None)
    assert config.polling_interval == 60
    assert config.theme == "auto"
    assert config.mode == "dashboard"
    assert config.providers == {}


def test_provider_config_log_path_expanded():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
        f.write(SAMPLE_TOML)
        f.flush()
        config = load_config(Path(f.name))
    os.unlink(f.name)

    assert "~" not in str(config.providers["openai"].log_path)
