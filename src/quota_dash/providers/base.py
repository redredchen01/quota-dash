from __future__ import annotations

from abc import ABC, abstractmethod

from quota_dash.models import QuotaInfo, TokenUsage, ContextInfo


class Provider(ABC):
    name: str

    @abstractmethod
    async def get_quota(self) -> QuotaInfo:
        ...

    @abstractmethod
    async def get_token_usage(self) -> TokenUsage:
        ...

    @abstractmethod
    async def get_context_window(self) -> ContextInfo:
        ...
