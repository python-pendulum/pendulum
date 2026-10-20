from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import timezone
from functools import partial
from typing import TYPE_CHECKING

import pytest

import pendulum


if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    "factory",
    [date, partial(datetime, tzinfo=timezone.utc), pendulum.date, pendulum.datetime],
)
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("absolute", [False, True])
def test_interval_membership_includes_both_endpoints(
    factory: Callable[[int, int, int], date], reverse: bool, absolute: bool
) -> None:
    first = factory(2024, 1, 10)
    last = factory(2024, 1, 12)
    start, end = (last, first) if reverse else (first, last)
    interval = pendulum.Interval(start, end, absolute=absolute)

    for day in (10, 11, 12):
        assert factory(2024, 1, day) in interval
    for day in (9, 13):
        assert factory(2024, 1, day) not in interval

    assert interval.start == (first if absolute else start)
    assert interval.end == (last if absolute else end)


@pytest.mark.parametrize(
    "factory",
    [date, partial(datetime, tzinfo=timezone.utc), pendulum.date, pendulum.datetime],
)
def test_single_point_interval_membership(
    factory: Callable[[int, int, int], date],
) -> None:
    point = factory(2024, 1, 10)
    interval = pendulum.Interval(point, point)
    assert point in interval
    assert factory(2024, 1, 9) not in interval
    assert factory(2024, 1, 11) not in interval


def test_inverted_interval_membership_with_different_offsets() -> None:
    start = pendulum.datetime(2024, 1, 10, 16, tz="Europe/Paris")
    end = pendulum.datetime(2024, 1, 10, 9, tz="America/New_York")
    interval = pendulum.Interval(start, end)
    assert pendulum.datetime(2024, 1, 10, 14, 30, tz="UTC") in interval
    assert pendulum.datetime(2024, 1, 10, 13, 59, tz="UTC") not in interval
    assert pendulum.datetime(2024, 1, 10, 15, 1, tz="UTC") not in interval
