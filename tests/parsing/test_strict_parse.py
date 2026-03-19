import pytest

from pendulum.parser import (
    parse_datetime,
    parse_date,
    parse_time,
    parse_duration,
)

# tests for parse_datetime


def test_parse_datetime_valid() -> None:
    dt = parse_datetime("2026-03-19T11:28:37")
    assert dt.year == 2026


def test_parse_datetime_accepts_date() -> None:
    dt = parse_datetime("2026-03-19")
    assert dt.hour == 0


def test_parse_datetime_rejects_interval() -> None:
    with pytest.raises(ValueError):
        parse_datetime("2026-03-19T12:00:00/2026-03-19T13:00:00")


def test_parse_datetime_accepts_only_year() -> None:
    dt = parse_datetime("2026")
    assert dt.year == 2026


# tests for parse_date


def test_parse_date_valid() -> None:
    d = parse_date("2026-03-19")
    assert d.day == 19


def test_parse_date_accepts_datetime() -> None:
    with pytest.raises(ValueError):
        parse_date("2026-03-19T11:28:37")


# tests for parse_time


def test_parse_time_valid() -> None:
    t = parse_time("11:28:37")
    assert t.hour == 11


def test_parse_time_accepts_datetime() -> None:
    with pytest.raises(ValueError):
        parse_time("2026-03-19T11:28:37")


# tests for parse_duration


def test_parse_duration_valid() -> None:
    dur = parse_duration("PT2H")
    assert dur.hours == 2


def test_parse_duration_rejects_datetime() -> None:
    with pytest.raises(ValueError):
        parse_duration("2026-03-19T11:28:37")
