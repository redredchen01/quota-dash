from __future__ import annotations

from textual.widget import Widget

from quota_dash.models import ContextInfo


class ContextGauge(Widget):
    DEFAULT_CSS = """
    ContextGauge {
        height: auto;
        min-height: 4;
        padding: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._data: ContextInfo | None = None

    def update_data(self, data: ContextInfo) -> None:
        self._data = data
        self.refresh()

    def render(self) -> str:
        if self._data is None:
            return "Context: loading..."

        d = self._data
        bar_width = 30
        filled = int(bar_width * d.percent_used / 100)
        bar = "█" * filled + "░" * (bar_width - filled)

        def fmt(n: int) -> str:
            if n >= 1000:
                return f"{n // 1000}K"
            return str(n)

        note = f"  ~ {d.note}" if d.note else ""
        lines = [
            f"Context Window ({d.model})",
            f"  {bar}  {d.percent_used:.0f}%",
            f"  {fmt(d.used_tokens)} / {fmt(d.max_tokens)}{note}",
        ]
        return "\n".join(lines)
