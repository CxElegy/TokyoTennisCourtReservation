"""えどねっと (https://www.shisetsuyoyaku.city.edogawa.tokyo.jp/user/Home).

The site is an ASP.NET Core + Vue (bootstrap-vue/axios) app. Navigation buttons call
`api/Header/Move*` and then redirect, so it is driven with a real browser (Playwright).

Login flow (confirmed):
  /user/Home → header「ログイン」button → /user/Login
  fields: UserLoginInputModel.Id / UserLoginInputModel.Password → footer「ログイン」button

TODO: availability (空き照会) flow
  施設種別 → 室場の分類 → 室場の種類 [テニスコート] → 施設名 → 空き表.
  Record the XHR endpoints once, then implement fetch_available().

robots.txt on this host disallows everything except /user/Home and *.html, so keep the
request rate low (see min_interval_minutes) and do not add retries/loops that hammer it.
"""

from __future__ import annotations

import os
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from ..models import Slot
from .base import Site

BASE_URL = "https://www.shisetsuyoyaku.city.edogawa.tokyo.jp/user"


@dataclass
class LoginResult:
    ok: bool
    url: str
    message: str = ""


def _launch(p):
    # In the Claude Code cloud container Chromium is preinstalled; elsewhere use
    # `playwright install chromium` and leave PLAYWRIGHT_CHROMIUM_PATH unset.
    path = os.environ.get("PLAYWRIGHT_CHROMIUM_PATH")
    return p.chromium.launch(executable_path=path) if path else p.chromium.launch()


class EdogawaSite(Site):
    name = "edogawa"

    def __init__(self, user_id: str | None = None, password: str | None = None):
        self.user_id = user_id or os.environ.get("EDOGAWA_USER_ID", "")
        self.password = password or os.environ.get("EDOGAWA_PASSWORD", "")

    def login(self, screenshot: str | Path | None = None) -> LoginResult:
        """Log in once and report whether it worked. Credentials are never logged."""
        if not self.user_id or not self.password:
            return LoginResult(False, "", "EDOGAWA_USER_ID / EDOGAWA_PASSWORD are not set")

        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = _launch(p)
            page = browser.new_page()
            try:
                page.goto(f"{BASE_URL}/Home", wait_until="networkidle")
                page.locator(".header .login button").click(force=True)
                page.wait_for_url("**/user/Login", timeout=15000)

                page.fill("#UserLoginInputModel_Id", self.user_id)
                page.fill("input[name='UserLoginInputModel.Password']", self.password)
                # The footer button is aria-hidden, so get_by_role() cannot see it.
                page.locator("button.btn-primary", has_text="ログイン").last.click()
                page.wait_for_load_state("networkidle")
                with suppress(PlaywrightTimeoutError):
                    page.wait_for_url(lambda u: "/user/Login" not in u, timeout=10000)

                if screenshot:
                    Path(screenshot).parent.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(screenshot), full_page=True)

                if "/user/Login" in page.url:
                    # Errors are shown in a bootstrap-vue modal (e.g. 利用者IDまたはパスワードが間違っています。)
                    errors = page.locator(".modal-body, .text-danger, .alert, .invalid-feedback")
                    texts = [t.strip() for t in errors.all_inner_texts() if t.strip()]
                    return LoginResult(False, page.url, " / ".join(texts) or "still on login page")
                return LoginResult(True, page.url)
            finally:
                browser.close()

    def fetch_available(self, facility_names: list[str]) -> list[Slot]:
        raise NotImplementedError(
            "えどねっと availability fetching is not implemented yet; see the module docstring."
        )
