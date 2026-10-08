from __future__ import annotations

import datetime

from zoneinfo import ZoneInfo

import pytest

from pendulum import Time
from tests.conftest import assert_time


def test_replace():
    t = Time(12, 34, 56, 123456)
    t = t.replace(1, 2, 3, 654321)

    assert isinstance(t, Time)
    assert_time(t, 1, 2, 3, 654321)


@pytest.mark.parametrize("original_fold", [0, 1])
@pytest.mark.parametrize("replacement_fold", [None, 0, 1])
def test_replace_fold_matches_native_time(
    original_fold: int, replacement_fold: int | None
) -> None:
    native = datetime.time(
        1, 30, tzinfo=ZoneInfo("America/New_York"), fold=original_fold
    )
    t = Time.instance(native)
    if replacement_fold is None:
        expected = native.replace(minute=45)
        actual = t.replace(minute=45)
    else:
        expected = native.replace(minute=45, fold=replacement_fold)
        actual = t.replace(minute=45, fold=replacement_fold)

    assert isinstance(actual, Time)
    assert actual.fold == expected.fold
    assert actual.tzinfo is t.tzinfo
    day = datetime.date(2026, 11, 1)
    assert datetime.datetime.combine(day, actual).astimezone(datetime.timezone.utc) == (
        datetime.datetime.combine(day, expected).astimezone(datetime.timezone.utc)
    )
