from __future__ import annotations

from .base import Notifier


class ConsoleNotifier(Notifier):
    def send(self, text: str) -> None:
        print(text)
