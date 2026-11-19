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


def test_multiply_float():
    # A float factor must scale years and months just like an int factor (and
    # like float division already does). Regression: Duration.__mul__ with a
    # float dropped the years/months components entirely.
    it = pendulum.duration(
        years=2, months=3, weeks=4, days=6, seconds=34, microseconds=522222
    )
    mul = it * 2.0

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 4, 6, 9, 5, 0, 1, 9, 44444)

    mul = 2.0 * it

    assert isinstance(mul, pendulum.Duration)
    assert_duration(mul, 4, 6, 9, 5, 0, 1, 9, 44444)

    # A whole-valued float must match the integer result exactly.
    it = pendulum.duration(years=1, months=6, days=2, seconds=35, microseconds=522222)
    by_int = it * 3
    by_float = it * 3.0

    assert (by_float.years, by_float.months) == (by_int.years, by_int.months)
    assert by_float.total_seconds() == by_int.total_seconds()

    # A non-integer factor rounds years/months, mirroring float division.
    it = pendulum.duration(years=2, months=4, days=2, seconds=35, microseconds=522222)
    mul = it * 1.5

    assert isinstance(mul, pendulum.Duration)
    assert mul.years == 3
    assert mul.months == 6


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
