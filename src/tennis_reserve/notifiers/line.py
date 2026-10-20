from __future__ import annotations

import os

import httpx

from .base import Notifier


class LineNotifier(Notifier):
    """LINE Messaging API push message (LINE Notify has been discontinued)."""

    def __init__(self, token: str | None = None, to: str | None = None):
        self.token = token or os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
        self.to = to or os.environ["LINE_TO"]

    def send(self, text: str) -> None:
        httpx.post(
            "https://api.line.me/v2/bot/message/push",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"to": self.to, "messages": [{"type": "text", "text": text}]},
            timeout=10,
        ).raise_for_status()
