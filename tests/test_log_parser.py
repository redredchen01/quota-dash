import json
import tempfile
from pathlib import Path

from quota_dash.data.log_parser import parse_claude_costs_jsonl, parse_codex_logs


def test_parse_claude_costs_jsonl_with_data():
    entries = [
        {"timestamp": "2026-03-20T10:00:00Z", "session_id": "s1", "model": "claude-opus-4-6", "input_tokens": 1500, "output_tokens": 800, "cost_usd": 0.05},
        {"timestamp": "2026-03-20T10:05:00Z", "session_id": "s1", "model": "claude-opus-4-6", "input_tokens": 2000, "output_tokens": 1200, "cost_usd": 0.07},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
        path = Path(f.name)

    result = parse_claude_costs_jsonl(path)
    assert result.input_tokens == 3500
    assert result.output_tokens == 2000
    assert result.total_tokens == 5500
    assert len(result.history) == 2
    path.unlink()


def test_parse_claude_costs_jsonl_all_zeros():
    entries = [
        {"timestamp": "2026-03-20T10:00:00Z", "session_id": "s1", "model": "unknown", "input_tokens": 0, "output_tokens": 0, "cost_usd": 0},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
        path = Path(f.name)

    result = parse_claude_costs_jsonl(path)
    assert result.total_tokens == 0
    assert result.source == "log"
    path.unlink()


def test_parse_claude_costs_jsonl_missing_file():
    result = parse_claude_costs_jsonl(Path("/nonexistent/costs.jsonl"))
    assert result.total_tokens == 0
    assert result.source == "estimated"


def test_parse_codex_logs_missing_file():
    result = parse_codex_logs(Path("/nonexistent/logs.sqlite"))
    assert result.total_tokens == 0
    assert result.source == "estimated"
