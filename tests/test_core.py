from datetime import UTC, date, datetime, time

from tennis_reserve.diff import filter_slots, new_slots
from tennis_reserve.models import Slot, WatchRule
from tennis_reserve.notifiers.base import format_message
from tennis_reserve.storage import State


def slot(day=date(2026, 11, 7), start=time(9), end=time(11), facility="水辺のスポーツガーデン"):
    return Slot(facility, "A面", day, start, end)


def test_rule_matches_weekday_and_time():
    rule = WatchRule("水辺", ("sat", "sun"), time(8), time(18))
    assert rule.matches(slot())  # 2026-11-07 is Saturday
    assert not rule.matches(slot(day=date(2026, 11, 9)))  # Monday
    assert not rule.matches(slot(start=time(6), end=time(8)))
    assert not rule.matches(slot(facility="西葛西"))


def test_filter_and_diff():
    rule = WatchRule("水辺", ("sat",), time(8), time(18))
    a, b = slot(), slot(day=date(2026, 11, 14))
    kept = filter_slots([a, b, slot(day=date(2026, 11, 9))], [rule])
    assert kept == [a, b]
    assert new_slots(kept, {a.key}) == [b]


def test_state_roundtrip(tmp_path):
    st = State(tmp_path / "s.json")
    assert st.previous_keys() == set() and st.last_run() is None
    now = datetime(2026, 11, 1, tzinfo=UTC)
    st.save({"k"}, now)
    assert st.previous_keys() == {"k"} and st.last_run() == now


def test_message():
    assert "1件" in format_message([slot()])
