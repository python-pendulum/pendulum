from __future__ import annotations

import operator

from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_duration


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


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
@pytest.mark.parametrize("reverse", [False, True])
def test_calendar_duration_arithmetic_with_interval(operation, reverse):
    start = pendulum.datetime(2024, 1, 1)
    interval = pendulum.interval(start, start.add(months=1))
    duration = pendulum.duration(months=1)
    left, right = (duration, interval) if reverse else (interval, duration)
    native_left, native_right = (
        (timedelta(days=30), timedelta(days=31))
        if reverse
        else (timedelta(days=31), timedelta(days=30))
    )
    assert operation(left, right) == operation(native_left, native_right)
