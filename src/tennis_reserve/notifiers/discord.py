from __future__ import annotations

import os

import httpx

from .base import Notifier


class DiscordNotifier(Notifier):
    def __init__(self, url: str | None = None):
        self.url = url or os.environ["DISCORD_WEBHOOK_URL"]

    def send(self, text: str) -> None:
        httpx.post(self.url, json={"content": text}, timeout=10).raise_for_status()
