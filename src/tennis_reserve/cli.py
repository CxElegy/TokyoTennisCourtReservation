from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv

from .config import load_config
from .diff import filter_slots, new_slots
from .notifiers import get_notifier
from .notifiers.base import format_message
from .sites import get_site
from .storage import State


def check(config_path: str, state_path: str, force: bool = False) -> int:
    cfg = load_config(config_path)
    state = State(state_path)

    last = state.last_run()
    now = datetime.now(UTC)
    if last and not force and now - last < timedelta(minutes=cfg.min_interval_minutes):
        print(f"skip: last run {last.isoformat()} is within {cfg.min_interval_minutes} min")
        return 0

    site = get_site(cfg.site)
    available = filter_slots(site.fetch_available([r.name for r in cfg.watch]), cfg.watch)
    fresh = new_slots(available, state.previous_keys())

    if fresh:
        text = format_message(fresh)
        for name in cfg.notifiers:
            get_notifier(name).send(text)
    else:
        print("no new availability")

    state.save({s.key for s in available}, now)
    return 0


def login(screenshot: str) -> int:
    from .sites.edogawa import EdogawaSite

    result = EdogawaSite().login(screenshot=screenshot)
    print(f"login {'OK' if result.ok else 'FAILED'}: {result.url} {result.message}".rstrip())
    print(f"screenshot: {screenshot}")
    return 0 if result.ok else 1


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    p = argparse.ArgumentParser(prog="tennis-reserve")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="fetch availability and notify about newly opened slots")
    c.add_argument("--config", default="config/facilities.yaml")
    c.add_argument("--state", default="data/state.json")
    c.add_argument("--force", action="store_true", help="ignore min_interval_minutes")
    lg = sub.add_parser("login", help="try logging in to えどねっと with EDOGAWA_* env vars")
    lg.add_argument("--screenshot", default="data/login.png")
    args = p.parse_args(argv)
    if args.cmd == "login":
        return login(args.screenshot)
    return check(args.config, args.state, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
