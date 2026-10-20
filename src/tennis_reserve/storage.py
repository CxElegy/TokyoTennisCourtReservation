from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


class State:
    """Tiny JSON file holding the last snapshot and last request time."""

    def __init__(self, path: str | Path = "data/state.json"):
        self.path = Path(path)

    def _read(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def previous_keys(self) -> set[str]:
        return set(self._read().get("keys", []))

    def last_run(self) -> datetime | None:
        value = self._read().get("last_run")
        return datetime.fromisoformat(value) if value else None

    def save(self, keys: set[str], now: datetime | None = None) -> None:
        now = now or datetime.now(UTC)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"keys": sorted(keys), "last_run": now.isoformat()}, ensure_ascii=False),
            encoding="utf-8",
        )
