from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import pendulum


if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize("factory", [pendulum.date, pendulum.datetime])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("absolute", [False, True])
@pytest.mark.parametrize("amount", [0, -1, -2])
def test_range_rejects_nonpositive_amount(
    factory: Callable[[int, int, int], pendulum.Date],
    reverse: bool,
    absolute: bool,
    amount: int,
) -> None:
    start = factory(2024, 1, 10)
    end = factory(2024, 1, 14)
    if reverse:
        start, end = end, start
    interval = pendulum.Interval(start, end, absolute=absolute)
    with pytest.raises(ValueError, match="amount must be positive"):
        next(interval.range("days", amount))


@pytest.mark.parametrize("amount", [0, -1])
def test_single_point_range_rejects_nonpositive_amount(amount: int) -> None:
    point = pendulum.date(2024, 1, 10)
    interval = pendulum.Interval(point, point)
    with pytest.raises(ValueError, match="amount must be positive"):
        next(interval.range("days", amount))


@pytest.mark.parametrize("factory", [pendulum.date, pendulum.datetime])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("amount", [1, 2, 3, 5])
def test_positive_range_amount_uses_interval_direction(
    factory: Callable[[int, int, int], pendulum.Date], reverse: bool, amount: int
) -> None:
    start = factory(2024, 1, 10)
    end = factory(2024, 1, 14)
    if reverse:
        start, end = end, start
    interval = pendulum.Interval(start, end)
    direction = -1 if reverse else 1
    expected = [
        factory(2024, 1, day)
        for day in range(start.day, end.day + direction, direction * amount)
    ]
    assert list(interval.range("days", amount)) == expected
