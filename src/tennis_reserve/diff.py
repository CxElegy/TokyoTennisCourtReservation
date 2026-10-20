from __future__ import annotations

from collections.abc import Iterable

from .models import Slot, WatchRule


def filter_slots(slots: Iterable[Slot], rules: list[WatchRule]) -> list[Slot]:
    return [s for s in slots if any(r.matches(s) for r in rules)]


def new_slots(current: Iterable[Slot], previous_keys: set[str]) -> list[Slot]:
    """Slots that are available now but were not in the previous snapshot."""
    return [s for s in current if s.key not in previous_keys]
