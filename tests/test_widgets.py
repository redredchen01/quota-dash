from datetime import datetime

import pytest
from textual.app import App, ComposeResult

from quota_dash.models import QuotaInfo, TokenUsage, ContextInfo
from quota_dash.widgets.provider_list import ProviderList
from quota_dash.widgets.quota_panel import QuotaPanel
from quota_dash.widgets.token_panel import TokenPanel
from quota_dash.widgets.context_gauge import ContextGauge


class WidgetTestApp(App):
    def compose(self) -> ComposeResult:
        yield ProviderList()
        yield QuotaPanel()
        yield TokenPanel()
        yield ContextGauge()


@pytest.mark.asyncio
async def test_widgets_mount():
    app = WidgetTestApp()
    async with app.run_test() as pilot:
        assert app.query_one(ProviderList) is not None
        assert app.query_one(QuotaPanel) is not None
        assert app.query_one(TokenPanel) is not None
        assert app.query_one(ContextGauge) is not None


@pytest.mark.asyncio
async def test_quota_panel_update():
    app = WidgetTestApp()
    async with app.run_test() as pilot:
        panel = app.query_one(QuotaPanel)
        panel.update_data(QuotaInfo(
            provider="openai", balance_usd=47.32, limit_usd=100.0,
            usage_today_usd=3.20, last_updated=datetime.now(),
            source="api", stale=False,
        ))
        await pilot.pause()
        assert panel.render is not None


@pytest.mark.asyncio
async def test_provider_list_set_providers():
    app = WidgetTestApp()
    async with app.run_test() as pilot:
        plist = app.query_one(ProviderList)
        plist.set_providers(["openai", "anthropic"])
        await pilot.pause()
        assert plist.render is not None
