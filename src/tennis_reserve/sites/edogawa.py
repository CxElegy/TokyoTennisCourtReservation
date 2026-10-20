"""えどねっと (https://www.shisetsuyoyaku.city.edogawa.tokyo.jp/user/Home).

Phase 1 skeleton. The site is an ASP.NET Core + Vue (bootstrap-vue/axios) app, so the
availability data most likely comes from JSON XHR calls behind the "空き照会・申込" flow
(施設種別 → 室場の分類 → 室場の種類 [テニスコート] → 施設名 → 空き表).

TODO (needs a one-time manual inspection with browser devtools / Playwright):
  1. Walk the flow above once and record the XHR endpoints and payloads.
  2. Implement fetch_available() either via those endpoints (preferred) or Playwright.
  3. Save a sample response under tests/fixtures/ and add a parser test.

robots.txt on this host disallows everything except /user/Home and *.html, so keep the
request rate low (see min_interval_minutes) and do not add retries/loops that hammer it.
"""

from __future__ import annotations

from ..models import Slot
from .base import Site


class EdogawaSite(Site):
    name = "edogawa"

    def fetch_available(self, facility_names: list[str]) -> list[Slot]:
        raise NotImplementedError(
            "えどねっと scraping is not implemented yet; see the module docstring for next steps."
        )
