from __future__ import annotations

from datetime import timedelta

import pendulum

from tests.conftest import assert_duration


def test_add_interval():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = pendulum.duration(days=12, seconds=30)

    p = p1 + p2
    assert_duration(p, 0, 0, 5, 0, 0, 1, 2)


def test_add_timedelta():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = timedelta(days=12, seconds=30)

    p = p1 + p2
    assert_duration(p, 0, 0, 5, 0, 0, 1, 2)


def test_add_unsupported():
    p = pendulum.duration(days=23, seconds=32)
    assert NotImplemented == p.__add__(5)


def test_sub_interval():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = pendulum.duration(days=12, seconds=28)

    p = p1 - p2
    assert_duration(p, 0, 0, 1, 4, 0, 0, 4)


def test_sub_timedelta():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = timedelta(days=12, seconds=28)

    p = p1 - p2
    assert_duration(p, 0, 0, 1, 4, 0, 0, 4)


def test_sub_unsupported():
    p = pendulum.duration(days=23, seconds=32)
    assert NotImplemented == p.__sub__(5)


def test_add_preserves_years_and_months():
    total = pendulum.duration(years=2) + pendulum.duration(days=1)
    assert_duration(total, years=2, months=0, weeks=0, days=1)

    months = pendulum.duration(months=2) + pendulum.duration(days=1)
    assert_duration(months, years=0, months=2, days=1)

    combined = pendulum.duration(years=1) + pendulum.duration(years=1)
    assert combined.years == 2
    assert combined.months == 0


def test_adding_year_durations_matches_successive_datetime_adds():
    start = pendulum.datetime(2023, 1, 1, tz="UTC")
    stepwise = (start + pendulum.duration(years=1)) + pendulum.duration(years=1)
    combined = start + (pendulum.duration(years=1) + pendulum.duration(years=1))

    assert stepwise == combined
    assert combined == pendulum.datetime(2025, 1, 1, tz="UTC")


def test_sub_preserves_years():
    difference = pendulum.duration(years=2, days=3) - pendulum.duration(years=1, days=1)
    assert_duration(difference, years=1, days=2)


def test_neg():
    p = pendulum.duration(days=23, seconds=32)
    assert_duration(-p, 0, 0, -3, -2, 0, 0, -32)
