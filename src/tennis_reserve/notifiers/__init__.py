from __future__ import annotations

from .base import Notifier
from .console import ConsoleNotifier


def get_notifier(name: str) -> Notifier:
    if name == "console":
        return ConsoleNotifier()
    if name == "discord":
        from .discord import DiscordNotifier

        return DiscordNotifier()
    if name == "line":
        from .line import LineNotifier

        return LineNotifier()
    if name == "email":
        from .email import EmailNotifier

        return EmailNotifier()
    raise ValueError(f"unknown notifier: {name}")
