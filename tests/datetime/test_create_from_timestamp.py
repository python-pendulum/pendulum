from __future__ import annotations

import pendulum

from pendulum import timezone
from tests.conftest import assert_datetime


def test_create_from_timestamp_returns_pendulum():
    d = pendulum.from_timestamp(pendulum.datetime(1975, 5, 21, 22, 32, 5).timestamp())
    assert_datetime(d, 1975, 5, 21, 22, 32, 5)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_before_epoch():
    d = pendulum.from_timestamp(-43201)
    assert_datetime(d, 1969, 12, 31, 11, 59, 59)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_with_timezone_string():
    d = pendulum.from_timestamp(0, "America/Toronto")
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)


def test_create_from_timestamp_with_timezone():
    d = pendulum.from_timestamp(0, timezone("America/Toronto"))
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)
