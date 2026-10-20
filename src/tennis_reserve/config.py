from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from pathlib import Path

import yaml

from .models import WatchRule


@dataclass
class Config:
    site: str
    min_interval_minutes: int
    notifiers: list[str]
    watch: list[WatchRule]


def _t(value: str) -> time:
    h, m = value.split(":")
    return time(int(h), int(m))


def load_config(path: str | Path) -> Config:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    rules = [
        WatchRule(
            name=w["name"],
            weekdays=tuple(w.get("weekdays", [])),
            time_from=_t(w.get("time_from", "00:00")),
            time_to=_t(w.get("time_to", "23:59")),
        )
        for w in raw.get("watch", [])
    ]
    return Config(
        site=raw.get("site", "edogawa"),
        min_interval_minutes=int(raw.get("min_interval_minutes", 30)),
        notifiers=list(raw.get("notifiers", ["console"])),
        watch=rules,
    )
