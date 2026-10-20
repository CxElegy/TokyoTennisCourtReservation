from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Slot


def format_message(slots: list[Slot]) -> str:
    lines = [f"🎾 テニスコートに空きが出ました（{len(slots)}件）"]
    lines += [f"・{s.label()}" for s in slots]
    return "\n".join(lines)


class Notifier(ABC):
    @abstractmethod
    def send(self, text: str) -> None: ...
