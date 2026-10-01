from __future__ import annotations

import pytest

import pendulum


@pytest.mark.parametrize("use_datetime", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("day", [1, 2, 3, 4, 5])
def test_membership_matches_interval_bounds(
    use_datetime: bool, reverse: bool, day: int
) -> None:
    start: pendulum.Date
    end: pendulum.Date
    item: pendulum.Date
    if use_datetime:
        start = pendulum.datetime(2026, 1, 2)
        end = pendulum.datetime(2026, 1, 4)
        item = pendulum.datetime(2026, 1, day)
    else:
        start = pendulum.date(2026, 1, 2)
        end = pendulum.date(2026, 1, 4)
        item = pendulum.date(2026, 1, day)
    interval = (
        pendulum.Interval(end, start) if reverse else pendulum.Interval(start, end)
    )
    assert (item in interval) == (2 <= day <= 4)
