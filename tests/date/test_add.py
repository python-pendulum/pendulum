from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_date


def test_add_years_positive():
    assert pendulum.date(1975, 1, 1).add(years=1).year == 1976


def test_add_years_zero():
    assert pendulum.date(1975, 1, 1).add(years=0).year == 1975


def test_add_years_negative():
    assert pendulum.date(1975, 1, 1).add(years=-1).year == 1974


def test_add_months_positive():
    assert pendulum.date(1975, 12, 1).add(months=1).month == 1


def test_add_months_zero():
    assert pendulum.date(1975, 12, 1).add(months=0).month == 12


def test_add_months_negative():
    assert pendulum.date(1975, 12, 1).add(months=-1).month == 11


def test_add_month_with_overflow():
    assert pendulum.Date(2012, 1, 31).add(months=1).month == 2


def test_add_days_positive():
    assert pendulum.Date(1975, 5, 31).add(days=1).day == 1


def test_add_days_zero():
    assert pendulum.Date(1975, 5, 31).add(days=0).day == 31


def test_add_days_negative():
    assert pendulum.Date(1975, 5, 31).add(days=-1).day == 30


def test_add_weeks_positive():
    assert pendulum.Date(1975, 5, 21).add(weeks=1).day == 28


def test_add_weeks_zero():
    assert pendulum.Date(1975, 5, 21).add(weeks=0).day == 21


def test_add_weeks_negative():
    assert pendulum.Date(1975, 5, 21).add(weeks=-1).day == 14


def test_add_timedelta():
    delta = timedelta(days=18)
    d = pendulum.date(2015, 3, 14)

    new = d + delta
    assert isinstance(new, pendulum.Date)
    assert_date(new, 2015, 4, 1)


def test_add_duration():
    duration = pendulum.duration(years=2, months=3, days=18)
    d = pendulum.Date(2015, 3, 14)

    new = d + duration
    assert_date(new, 2017, 7, 2)


def test_addition_invalid_type():
    d = pendulum.date(2015, 3, 14)

    with pytest.raises(TypeError):
        d + 3

    with pytest.raises(TypeError):
        3 + d


def test_add_rejects_bool():
    import pytest

    d = pendulum.date(2020, 5, 15)
    for key in ("years", "months", "weeks", "days"):
        with pytest.raises(TypeError, match=key):
            d.add(**{key: True})
