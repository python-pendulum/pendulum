from __future__ import annotations

import operator

from datetime import timedelta
from typing import TYPE_CHECKING

import pytest

import pendulum

from tests.conftest import assert_duration


if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
@pytest.mark.parametrize(
    "divisor", [timedelta(days=1), timedelta(seconds=-2), timedelta(microseconds=3)]
)
def test_arithmetic_with_standard_timedelta(
    operation: Callable[[timedelta, timedelta], object], divisor: timedelta
) -> None:
    expected = timedelta(days=2, seconds=35, microseconds=522222)
    duration = pendulum.duration(days=2, seconds=35, microseconds=522222)
    assert operation(duration, divisor) == operation(expected, divisor)


@pytest.mark.parametrize(
    "operation", [operator.truediv, operator.floordiv, operator.mod, divmod]
)
def test_arithmetic_with_zero_timedelta(
    operation: Callable[[timedelta, timedelta], object],
) -> None:
    with pytest.raises(ZeroDivisionError):
        operation(pendulum.duration(seconds=1), timedelta())


def test_timedelta_divisor_keeps_large_microsecond_precision() -> None:
    divisor = timedelta(days=200000, microseconds=1)
    assert pendulum.duration(days=200000) // divisor == 0


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
