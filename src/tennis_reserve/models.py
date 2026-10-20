from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True)
class Slot:
    """One bookable court slot."""

    facility: str
    court: str
    day: date
    start: time
    end: time

    @property
    def key(self) -> str:
        return f"{self.facility}|{self.court}|{self.day.isoformat()}|{self.start:%H:%M}-{self.end:%H:%M}"

    def label(self) -> str:
        return (
            f"{self.facility} {self.court} {self.day:%m/%d}({'月火水木金土日'[self.day.weekday()]}) "
            f"{self.start:%H:%M}-{self.end:%H:%M}"
        )


@dataclass(frozen=True)
class WatchRule:
    name: str
    weekdays: tuple[str, ...] = ()
    time_from: time = time(0, 0)
    time_to: time = time(23, 59)

    def matches(self, slot: Slot) -> bool:
        if self.name not in slot.facility:
            return False
        if self.weekdays:
            wd = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"][slot.day.weekday()]
            # "holiday" needs a holiday calendar; not implemented yet (see docs/overview.md).
            if wd not in self.weekdays:
                return False
        return slot.start >= self.time_from and slot.end <= self.time_to
