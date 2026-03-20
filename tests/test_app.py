import pytest
from quota_dash.app import QuotaDashApp
from quota_dash.widgets.quota_panel import QuotaPanel
from quota_dash.config import AppConfig, ProviderConfig
from pathlib import Path


@pytest.mark.asyncio
async def test_app_launches():
    app = QuotaDashApp()
    async with app.run_test() as pilot:
        assert app.title == "quota-dash"


@pytest.mark.asyncio
async def test_app_quit_binding():
    app = QuotaDashApp()
    async with app.run_test() as pilot:
        await pilot.press("q")


@pytest.mark.asyncio
async def test_app_refresh_binding():
    app = QuotaDashApp()
    async with app.run_test() as pilot:
        await pilot.press("r")


@pytest.mark.asyncio
async def test_app_with_manual_config():
    config = AppConfig(
        polling_interval=60,
        theme="default",
        providers={
            "openai": ProviderConfig(
                enabled=True, api_key_env="NONEXISTENT",
                log_path=Path("/tmp/nonexistent"),
                balance_usd=50.0, limit_usd=100.0,
            ),
        },
    )
    app = QuotaDashApp(config=config)
    async with app.run_test() as pilot:
        assert app.title == "quota-dash"
        await pilot.press("r")
        await pilot.pause()
        panel = app.query_one(QuotaPanel)
        assert panel is not None
