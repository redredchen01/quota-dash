from datetime import datetime

from quota_dash.data.store import DataStore
from quota_dash.models import QuotaInfo, TokenUsage, ContextInfo


def test_store_update_provider():
    store = DataStore()
    quota = QuotaInfo(
        provider="openai", balance_usd=47.32, limit_usd=100.0,
        usage_today_usd=3.20, last_updated=datetime.now(),
        source="api", stale=False,
    )
    store.update_quota("openai", quota)
    assert store.get_quota("openai") == quota


def test_store_get_missing_provider():
    store = DataStore()
    assert store.get_quota("nonexistent") is None


def test_store_aggregate_balance():
    store = DataStore()
    store.update_quota("openai", QuotaInfo(
        provider="openai", balance_usd=47.32, limit_usd=100.0,
        usage_today_usd=3.20, last_updated=datetime.now(),
        source="api", stale=False,
    ))
    store.update_quota("anthropic", QuotaInfo(
        provider="anthropic", balance_usd=100.0, limit_usd=200.0,
        usage_today_usd=1.50, last_updated=datetime.now(),
        source="manual", stale=False,
    ))
    assert store.total_balance() == 147.32
    assert store.total_usage_today() == 4.70


def test_store_aggregate_skips_none():
    store = DataStore()
    store.update_quota("openai", QuotaInfo(
        provider="openai", balance_usd=47.32, limit_usd=100.0,
        usage_today_usd=3.20, last_updated=datetime.now(),
        source="api", stale=False,
    ))
    store.update_quota("anthropic", QuotaInfo(
        provider="anthropic", balance_usd=None, limit_usd=None,
        usage_today_usd=None, last_updated=datetime.now(),
        source="unavailable", stale=False,
    ))
    assert store.total_balance() == 47.32
    assert store.total_usage_today() == 3.20
