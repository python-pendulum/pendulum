from __future__ import annotations

import operator

from datetime import timedelta

import pytest

import pendulum

from pendulum.duration import AbsoluteDuration
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


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
@pytest.mark.parametrize(
    ("left", "right"),
    [
        ({"months": 2}, {"months": 1}),
        ({"years": 1}, {"months": 1}),
        ({"months": 1}, {"days": 7}),
        ({"days": 7}, {"months": 1}),
        ({"years": -1, "months": 2, "days": -3}, {"months": 2, "days": 1}),
        ({"years": 1, "months": -2, "seconds": 3}, {"months": -2, "seconds": -1}),
        ({"months": 1, "days": -30}, {"years": 1}),
        ({"months": 1, "microseconds": 2}, {"months": 1, "microseconds": 1}),
    ],
)
def test_calendar_duration_quotient_and_remainder(operation, left, right):
    def native_duration(parts):
        fixed = {
            key: value for key, value in parts.items() if key not in ("years", "months")
        }
        fixed["days"] = (
            fixed.get("days", 0)
            + parts.get("years", 0) * 365
            + parts.get("months", 0) * 30
        )
        return timedelta(**fixed)

    result = operation(pendulum.duration(**left), pendulum.duration(**right))
    assert result == operation(native_duration(left), native_duration(right))


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
def test_calendar_duration_zero_divisor(operation):
    with pytest.raises(ZeroDivisionError):
        operation(pendulum.duration(months=1), pendulum.duration(months=1, days=-30))


@pytest.mark.parametrize("divisor", [2, 2.0])
def test_calendar_duration_scalar_division_unchanged(divisor):
    result = pendulum.duration(years=4, months=6, days=10) / divisor
    assert_duration(result, 2, 3, 0, 5, 0, 0, 0)


def test_calendar_duration_scalar_floor_division_unchanged():
    result = pendulum.duration(years=4, months=6, days=10) // 2
    assert_duration(result, 2, 3, 0, 5, 0, 0, 0)


def test_calendar_duration_remainder_preserves_subclass():
    class CustomDuration(pendulum.Duration):
        pass

    duration = CustomDuration(months=1)
    divisor = pendulum.duration(days=7)
    assert type(duration % divisor) is CustomDuration
    assert type(divmod(duration, divisor)[1]) is CustomDuration
    assert duration % divisor == timedelta(days=2)


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
@pytest.mark.parametrize(
    ("left", "right", "left_days", "right_days"),
    [
        (AbsoluteDuration(years=1, months=1), pendulum.duration(days=30), 395, 30),
        (pendulum.duration(months=2), AbsoluteDuration(months=1), 60, 30),
        (AbsoluteDuration(months=1), pendulum.duration(months=2), 30, 60),
        (AbsoluteDuration(years=-1), AbsoluteDuration(months=-1), 365, 30),
    ],
)
def test_calendar_duration_arithmetic_with_absolute_duration(
    operation, left, right, left_days, right_days
):
    assert operation(left, right) == operation(
        timedelta(days=left_days), timedelta(days=right_days)
    )
