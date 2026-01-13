from __future__ import annotations

import pickle

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
