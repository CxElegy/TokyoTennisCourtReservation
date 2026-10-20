from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from .base import Notifier


class EmailNotifier(Notifier):
    def send(self, text: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = "テニスコート空き通知"
        msg["From"] = os.environ["MAIL_FROM"]
        msg["To"] = os.environ["MAIL_TO"]
        msg.set_content(text)
        with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", "587"))) as s:
            s.starttls()
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
