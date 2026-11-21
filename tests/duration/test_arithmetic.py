from __future__ import annotations

import pendulum

from tests.conftest import assert_duration


def test_multiply():
    it = pendulum.duration(days=6, seconds=34, microseconds=522222)
    mul = it * 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 1, 5, 0, 1, 9, 44444)

    it = pendulum.duration(days=6, seconds=34, microseconds=522222)
    mul = 2 * it

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 1, 5, 0, 1, 9, 44444)

    it = pendulum.duration(
        years=2, months=3, weeks=4, days=6, seconds=34, microseconds=522222
    )
    mul = 2 * it

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 4, 6, 9, 5, 0, 1, 9, 44444)


def test_divide():
    it = pendulum.duration(days=2, seconds=34, microseconds=522222)
    mul = it / 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17, 261111)

    it = pendulum.duration(days=2, seconds=35, microseconds=522222)
    mul = it / 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17, 761111)

    it = pendulum.duration(days=2, seconds=35, microseconds=522222)
    mul = it / 1.1

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 19, 38, 43, 202020)

    it = pendulum.duration(years=2, months=4, days=2, seconds=35, microseconds=522222)
    mul = it / 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 1, 2, 0, 1, 0, 0, 17, 761111)

    it = pendulum.duration(years=2, months=4, days=2, seconds=35, microseconds=522222)
    mul = it / 2.0

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 1, 2, 0, 1, 0, 0, 17, 761111)


def test_floor_divide():
    it = pendulum.duration(days=2, seconds=34, microseconds=522222)
    mul = it // 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 1, 0, 0, 17, 261111)

    it = pendulum.duration(days=2, seconds=35, microseconds=522222)
    mul = it // 3

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 0, 0, 0, 16, 0, 11, 840740)

    it = pendulum.duration(years=2, months=4, days=2, seconds=34, microseconds=522222)
    mul = it // 2

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 1, 2, 0, 1, 0, 0, 17, 261111)

    it = pendulum.duration(years=2, months=4, days=2, seconds=35, microseconds=522222)
    mul = it // 3

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 0, 1, 0, 0, 16, 0, 11, 840740)


def test_abs():
    it = pendulum.duration(years=-2, months=-3, days=-10, seconds=-34, microseconds=-5)
    result = abs(it)

    assert isinstance(result, pendulum.Duration)
    assert_duration(result, 2, 3, 1, 3, 0, 0, 34, 5)

    it = pendulum.duration(years=2, months=3, days=10)
    result = abs(it)

    assert isinstance(result, pendulum.Duration)
    assert_duration(result, 2, 3, 1, 3, 0, 0, 0, 0)


def test_pos():
    it = pendulum.duration(years=2, months=3, days=10)
    result = +it

    assert isinstance(result, pendulum.Duration)
    assert_duration(result, 2, 3, 1, 3, 0, 0, 0, 0)
