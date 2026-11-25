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


@pytest.mark.parametrize(
    "duration, expected",
    [
        (
            pendulum.duration(years=2, months=3, weeks=1, days=2),
            {"years": 2, "months": 3, "weeks": 1, "days": 2},
        ),
        (
            pendulum.duration(years=-1, months=-5, weeks=-2, days=-3),
            {"years": -1, "months": -5, "weeks": -2, "days": -3},
        ),
        (
            pendulum.duration(
                years=1,
                months=-2,
                weeks=1,
                days=-4,
                hours=5,
                minutes=-6,
                seconds=7,
                microseconds=8,
            ),
            {
                "years": 1,
                "months": -2,
                "weeks": 0,
                "days": 3,
                "hours": 4,
                "minutes": 54,
                "seconds": 7,
                "microseconds": 8,
            },
        ),
        (
            pendulum.duration(microseconds=42),
            {
                "years": 0,
                "months": 0,
                "weeks": 0,
                "days": 0,
                "microseconds": 42,
            },
        ),
    ],
)
def test_pickle_preserves_calendar_units(duration, expected) -> None:
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        restored = pickle.loads(pickle.dumps(duration, protocol=protocol))

        assert restored == duration
        assert restored.total_seconds() == duration.total_seconds()
        assert str(restored) == str(duration)
        assert_duration(restored, **expected)


def test_copy_preserves_calendar_units() -> None:
    duration = pendulum.duration(years=2, months=3, weeks=1, days=2)
    copied = copy(duration)

    assert copied == duration
    assert_duration(copied, years=2, months=3, weeks=1, days=2)


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
