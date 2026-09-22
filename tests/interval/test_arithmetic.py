from __future__ import annotations

from datetime import timedelta

import pendulum

from tests.conftest import assert_duration


def test_arithmetic_with_standard_timedelta():
    start = pendulum.datetime(2019, 1, 1)
    interval = pendulum.interval(start, start.add(hours=25))
    day = timedelta(days=1)

    assert interval / day == 25 / 24
    assert interval // day == 1
    assert interval % day == timedelta(hours=1)
    assert divmod(interval, day) == (1, timedelta(hours=1))


def test_multiply():
    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=6, seconds=34)
    it = pendulum.interval(dt1, dt2)
    mul = it * 2
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 1, 5, 0, 1, 8)

    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=6, seconds=34)
    it = pendulum.interval(dt1, dt2)
    mul = it * 2
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 1, 5, 0, 1, 8)


def test_divide():
    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=2, seconds=34)
    it = pendulum.interval(dt1, dt2)
    mul = it / 2
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17)

    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=2, seconds=35)
    it = pendulum.interval(dt1, dt2)
    mul = it / 2
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17)


def test_floor_divide():
    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=2, seconds=34)
    it = pendulum.interval(dt1, dt2)
    mul = it // 2
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17)

    dt1 = pendulum.DateTime(2016, 8, 7, 12, 34, 56)
    dt2 = dt1.add(days=2, seconds=35)
    it = pendulum.interval(dt1, dt2)
    mul = it // 3
    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 0, 16, 0, 11)
