from __future__ import annotations

import pickle

from copy import copy
from copy import deepcopy
from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_duration


def test_pickle() -> None:
    it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
    s = pickle.dumps(it)
    it2 = pickle.loads(s)

    assert it == it2


@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
@pytest.mark.parametrize("years, months", [(2, 3), (-2, -3), (1, -2)])
def test_pickle_preserves_calendar_components(
    protocol: int, years: int, months: int
) -> None:
    original = pendulum.duration(
        years=years, months=months, weeks=1, days=2, seconds=37, microseconds=123
    )
    restored = pickle.loads(pickle.dumps(original, protocol=protocol))

    assert restored == original
    assert restored.years == original.years
    assert restored.months == original.months
    assert restored.weeks == original.weeks
    assert restored.remaining_days == original.remaining_days
    assert restored.seconds == original.seconds
    assert restored.microseconds == original.microseconds
    assert str(restored) == str(original)


def test_shallow_copy_preserves_calendar_components() -> None:
    original = pendulum.duration(years=1, months=2, days=9)
    copied = copy(original)

    assert copied is not original
    assert copied == original
    assert copied.years == original.years
    assert copied.months == original.months
    assert str(copied) == str(original)


def test_comparison_to_timedelta() -> None:
    duration = pendulum.duration(days=3)

    assert duration < timedelta(days=4)


@pytest.mark.parametrize(
    "duration, expected",
    [
        (pendulum.duration(months=1), {"months": 1}),
        (pendulum.Duration(days=9), {"weeks": 1, "days": 2}),
    ],
)
def test_deepcopy(duration, expected) -> None:
    copied_duration = deepcopy(duration)

    assert copied_duration == duration
    assert_duration(copied_duration, **expected)
