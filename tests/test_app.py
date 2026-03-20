import pytest
from quota_dash.app import QuotaDashApp


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
