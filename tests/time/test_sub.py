from __future__ import annotations

import zoneinfo

from datetime import time
from datetime import timedelta

import pytest

import pendulum

from pendulum import Time
from tests.conftest import assert_duration


def test_sub_hours_positive():
    assert Time(0, 0, 0).subtract(hours=1).hour == 23


def test_sub_hours_zero():
    assert Time(0, 0, 0).subtract(hours=0).hour == 0


def test_sub_hours_negative():
    assert Time(0, 0, 0).subtract(hours=-1).hour == 1


def test_sub_minutes_positive():
    assert Time(0, 0, 0).subtract(minutes=1).minute == 59


def test_sub_minutes_zero():
    assert Time(0, 0, 0).subtract(minutes=0).minute == 0


def test_sub_minutes_negative():
    assert Time(0, 0, 0).subtract(minutes=-1).minute == 1


def test_sub_seconds_positive():
    assert Time(0, 0, 0).subtract(seconds=1).second == 59


def test_sub_seconds_zero():
    assert Time(0, 0, 0).subtract(seconds=0).second == 0


def test_sub_seconds_negative():
    assert Time(0, 0, 0).subtract(seconds=-1).second == 1


def test_subtract_timedelta():
    delta = timedelta(seconds=16, microseconds=654321)
    d = Time(3, 12, 15, 777777)

    d = d.subtract_timedelta(delta)
    assert d.minute == 11
    assert d.second == 59
    assert d.microsecond == 123456

    d = Time(3, 12, 15, 777777)

    d = d - delta
    assert d.minute == 11
    assert d.second == 59
    assert d.microsecond == 123456


def test_add_timedelta_with_days():
    delta = timedelta(days=3, seconds=45, microseconds=123456)
    d = Time(3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d.subtract_timedelta(delta)


def test_subtract_invalid_type():
    d = Time(0, 0, 0)

    with pytest.raises(TypeError):
        d - "ab"

    with pytest.raises(TypeError):
        "ab" - d


def test_subtract_time():
    t = Time(12, 34, 56)
    t1 = Time(1, 1, 1)
    t2 = time(1, 1, 1)
    t3 = time(1, 1, 1, tzinfo=zoneinfo.ZoneInfo("Europe/Paris"))

    diff = t - t1
    assert isinstance(diff, pendulum.Duration)
    assert_duration(diff, 0, hours=11, minutes=33, seconds=55)

    diff = t1 - t
    assert isinstance(diff, pendulum.Duration)
    assert_duration(diff, 0, hours=-11, minutes=-33, seconds=-55)

    diff = t - t2
    assert isinstance(diff, pendulum.Duration)
    assert_duration(diff, 0, hours=11, minutes=33, seconds=55)

    diff = t2 - t
    assert isinstance(diff, pendulum.Duration)
    assert_duration(diff, 0, hours=-11, minutes=-33, seconds=-55)

    with pytest.raises(TypeError):
        t - t3

    with pytest.raises(TypeError):
        t3 - t
