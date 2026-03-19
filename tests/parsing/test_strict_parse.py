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

def test_parse_datetime_rejects_date() -> None:
    with pytest.raises(ValueError):
        dt = parse_datetime("2026-03-19")

def test_parse_datetime_rejects_interval() -> None:
    with pytest.raises(ValueError):
        dt = parse_datetime("2026-03-19T12:00:00/2026-03-19T13:00:00")

# tests for parse_date

def test_parse_date_valid() -> None:
    dt = parse_date("2026-03-19")
    assert dt.year == 2026

def test_parse_date_rejects_datetime() -> None:
    with pytest.raises(ValueError):
        dt = parse_date("2026-03-19T11:28:37")
