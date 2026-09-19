from __future__ import annotations

import datetime as datetime_

import pendulum
import pytest

from pendulum import timezone
from tests.conftest import assert_datetime


def test_create_from_timestamp_returns_pendulum():
    d = pendulum.from_timestamp(pendulum.datetime(1975, 5, 21, 22, 32, 5).timestamp())
    assert_datetime(d, 1975, 5, 21, 22, 32, 5)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_with_timezone_string():
    d = pendulum.from_timestamp(0, "America/Toronto")
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)


def test_create_from_timestamp_with_timezone():
    d = pendulum.from_timestamp(0, timezone("America/Toronto"))
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 19, 0, 0)


def test_create_from_timestamp_negative():
    d = pendulum.from_timestamp(-43201)
    assert_datetime(d, 1969, 12, 31, 11, 59, 59)
    assert d.timezone_name == "UTC"


def test_create_from_timestamp_negative_with_timezone():
    d = pendulum.from_timestamp(-43201, "America/Toronto")
    assert d.timezone_name == "America/Toronto"
    assert_datetime(d, 1969, 12, 31, 6, 59, 59)


def test_create_from_timestamp_negative_with_microseconds():
    d = pendulum.from_timestamp(-43201.5)
    assert_datetime(d, 1969, 12, 31, 11, 59, 58, 500000)
    assert d.timezone_name == "UTC"


@pytest.mark.parametrize("exception_type", [OSError, OverflowError])
def test_create_from_timestamp_falls_back_for_negative_timestamp(
    monkeypatch, exception_type
):
    class FakeDateTime(datetime_.datetime):
        @classmethod
        def fromtimestamp(cls, timestamp: float, tz: datetime_.tzinfo | None = None):
            if timestamp == -43201:
                raise exception_type("Invalid argument")

            return super().fromtimestamp(timestamp, tz=tz)

    monkeypatch.setattr(pendulum._datetime, "datetime", FakeDateTime)

    d = pendulum.from_timestamp(-43201)

    assert_datetime(d, 1969, 12, 31, 11, 59, 59)
    assert d.timezone_name == "UTC"
