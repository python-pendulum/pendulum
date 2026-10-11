from __future__ import annotations

from datetime import date

import pytest

import pendulum


@pytest.fixture
def today():
    return pendulum.Date.today()


def test_diff_in_years_positive():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_years() == 1


def test_diff_in_years_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_years() == -1


def test_diff_in_years_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_years() == 1


def test_diff_in_years_vs_default_now(today):
    assert today.subtract(years=1).diff().in_years() == 1


def test_diff_in_years_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(years=1).add(months=7)).in_years() == 1


def test_diff_in_months_positive():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(years=1).add(months=1)).in_months() == 13


def test_diff_in_months_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)

    assert dt.diff(dt.subtract(years=1).add(months=1), False).in_months() == -11


def test_diff_in_months_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1).add(months=1)).in_months() == 11


def test_diff_in_months_vs_default_now(today):
    assert today.subtract(years=1).diff().in_months() == 12


def test_diff_in_months_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(months=1).add(days=16)).in_months() == 1


def test_diff_in_days_positive():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_days() == 366


def test_diff_in_days_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_days() == -365


def test_diff_in_days_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_days() == 365


def test_diff_in_days_vs_default_now(today):
    assert today.subtract(weeks=1).diff().in_days() == 7


def test_diff_in_weeks_positive():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_weeks() == 52


def test_diff_in_weeks_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_weeks() == -52


def test_diff_in_weeks_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_weeks() == 52


def test_diff_in_weeks_vs_default_now(today):
    assert today.subtract(weeks=1).diff().in_weeks() == 1


def test_diff_in_weeks_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks() == 0


def test_diff_for_humans_now_and_day(today):
    assert today.subtract(days=1).diff_for_humans() == "1 day ago"


def test_diff_for_humans_now_and_days(today):
    assert today.subtract(days=2).diff_for_humans() == "2 days ago"


def test_diff_for_humans_now_and_nearly_week(today):
    assert today.subtract(days=6).diff_for_humans() == "6 days ago"


def test_diff_for_humans_now_and_week(today):
    assert today.subtract(weeks=1).diff_for_humans() == "1 week ago"


def test_diff_for_humans_now_and_weeks(today):
    assert today.subtract(weeks=2).diff_for_humans() == "2 weeks ago"


def test_diff_for_humans_now_and_nearly_month(today):
    assert today.subtract(weeks=3).diff_for_humans() == "3 weeks ago"


def test_diff_for_humans_now_and_month():
    with pendulum.travel_to(pendulum.datetime(2016, 4, 1)):
        today = pendulum.today().date()

        assert today.subtract(weeks=4).diff_for_humans() == "4 weeks ago"
        assert today.subtract(months=1).diff_for_humans() == "1 month ago"

    with pendulum.travel_to(pendulum.datetime(2017, 3, 1)):
        today = pendulum.today().date()

        assert today.subtract(weeks=4).diff_for_humans() == "1 month ago"


def test_diff_for_humans_now_and_months(today):
    assert today.subtract(months=2).diff_for_humans() == "2 months ago"


def test_diff_for_humans_now_and_nearly_year(today):
    assert today.subtract(months=11).diff_for_humans() == "11 months ago"


def test_diff_for_humans_now_and_year(today):
    assert today.subtract(years=1).diff_for_humans() == "1 year ago"


def test_diff_for_humans_now_and_years(today):
    assert today.subtract(years=2).diff_for_humans() == "2 years ago"


def test_diff_for_humans_now_and_future_day(today):
    assert today.add(days=1).diff_for_humans() == "in 1 day"


def test_diff_for_humans_now_and_future_days(today):
    assert today.add(days=2).diff_for_humans() == "in 2 days"


def test_diff_for_humans_now_and_nearly_future_week(today):
    assert today.add(days=6).diff_for_humans() == "in 6 days"


def test_diff_for_humans_now_and_future_week(today):
    assert today.add(weeks=1).diff_for_humans() == "in 1 week"


def test_diff_for_humans_now_and_future_weeks(today):
    assert today.add(weeks=2).diff_for_humans() == "in 2 weeks"


def test_diff_for_humans_now_and_nearly_future_month(today):
    assert today.add(weeks=3).diff_for_humans() == "in 3 weeks"


def test_diff_for_humans_now_and_future_month():
    with pendulum.travel_to(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today("UTC").date()

        assert today.add(weeks=4).diff_for_humans() == "in 4 weeks"
        assert today.add(months=1).diff_for_humans() == "in 1 month"

    with pendulum.travel_to(pendulum.datetime(2017, 3, 31)):
        today = pendulum.today("UTC").date()

        assert today.add(months=1).diff_for_humans() == "in 1 month"

    with pendulum.travel_to(pendulum.datetime(2017, 4, 30)):
        today = pendulum.today("UTC").date()

        assert today.add(months=1).diff_for_humans() == "in 1 month"

    with pendulum.travel_to(pendulum.datetime(2017, 1, 31)):
        today = pendulum.today("UTC").date()

        assert today.add(weeks=4).diff_for_humans() == "in 1 month"


def test_diff_for_humans_now_and_future_months(today):
    assert today.add(months=2).diff_for_humans() == "in 2 months"


def test_diff_for_humans_now_and_nearly_future_year(today):
    assert today.add(months=11).diff_for_humans() == "in 11 months"


def test_diff_for_humans_now_and_future_year(today):
    assert today.add(years=1).diff_for_humans() == "in 1 year"


def test_diff_for_humans_now_and_future_years(today):
    assert today.add(years=2).diff_for_humans() == "in 2 years"


def test_diff_for_humans_other_and_day(today):
    assert today.diff_for_humans(today.add(days=1)) == "1 day before"


def test_diff_for_humans_other_and_days(today):
    assert today.diff_for_humans(today.add(days=2)) == "2 days before"


def test_diff_for_humans_other_and_nearly_week(today):
    assert today.diff_for_humans(today.add(days=6)) == "6 days before"


def test_diff_for_humans_other_and_week(today):
    assert today.diff_for_humans(today.add(weeks=1)) == "1 week before"


def test_diff_for_humans_other_and_weeks(today):
    assert today.diff_for_humans(today.add(weeks=2)) == "2 weeks before"


def test_diff_for_humans_other_and_nearly_month(today):
    assert today.diff_for_humans(today.add(weeks=3)) == "3 weeks before"


def test_diff_for_humans_other_and_month():
    with pendulum.travel_to(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.add(weeks=4)) == "4 weeks before"
        assert today.diff_for_humans(today.add(months=1)) == "1 month before"

    with pendulum.travel_to(pendulum.datetime(2017, 3, 31)):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.add(months=1)) == "1 month before"

    with pendulum.travel_to(pendulum.datetime(2017, 4, 30)):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.add(months=1)) == "1 month before"

    with pendulum.travel_to(pendulum.datetime(2017, 1, 31, tz="America/Toronto")):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.add(weeks=4)) == "1 month before"


def test_diff_for_humans_other_and_months(today):
    assert today.diff_for_humans(today.add(months=2)) == "2 months before"


def test_diff_for_humans_other_and_nearly_year(today):
    assert today.diff_for_humans(today.add(months=11)) == "11 months before"


def test_diff_for_humans_other_and_year(today):
    assert today.diff_for_humans(today.add(years=1)) == "1 year before"


def test_diff_for_humans_other_and_years(today):
    assert today.diff_for_humans(today.add(years=2)) == "2 years before"


def test_diff_for_humans_other_and_future_day(today):
    assert today.diff_for_humans(today.subtract(days=1)) == "1 day after"


def test_diff_for_humans_other_and_future_days(today):
    assert today.diff_for_humans(today.subtract(days=2)) == "2 days after"


def test_diff_for_humans_other_and_nearly_future_week(today):
    assert today.diff_for_humans(today.subtract(days=6)) == "6 days after"


def test_diff_for_humans_other_and_future_week(today):
    assert today.diff_for_humans(today.subtract(weeks=1)) == "1 week after"


def test_diff_for_humans_other_and_future_weeks(today):
    assert today.diff_for_humans(today.subtract(weeks=2)) == "2 weeks after"


def test_diff_for_humans_other_and_nearly_future_month(today):
    assert today.diff_for_humans(today.subtract(weeks=3)) == "3 weeks after"


def test_diff_for_humans_other_and_future_month():
    with pendulum.travel_to(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.subtract(weeks=4)) == "4 weeks after"
        assert today.diff_for_humans(today.subtract(months=1)) == "1 month after"

    with pendulum.travel_to(pendulum.datetime(2017, 2, 28, tz="America/Toronto")):
        today = pendulum.today().date()

        assert today.diff_for_humans(today.subtract(weeks=4)) == "1 month after"


def test_diff_for_humans_other_and_future_months(today):
    assert today.diff_for_humans(today.subtract(months=2)) == "2 months after"


def test_diff_for_humans_other_and_nearly_future_year(today):
    assert today.diff_for_humans(today.subtract(months=11)) == "11 months after"


def test_diff_for_humans_other_and_future_year(today):
    assert today.diff_for_humans(today.subtract(years=1)) == "1 year after"


def test_diff_for_humans_other_and_future_years(today):
    assert today.diff_for_humans(today.subtract(years=2)) == "2 years after"


def test_diff_for_humans_absolute_days(today):
    assert today.diff_for_humans(today.subtract(days=2), True) == "2 days"
    assert today.diff_for_humans(today.add(days=2), True) == "2 days"


def test_diff_for_humans_absolute_weeks(today):
    assert today.diff_for_humans(today.subtract(weeks=2), True) == "2 weeks"
    assert today.diff_for_humans(today.add(weeks=2), True) == "2 weeks"


def test_diff_for_humans_absolute_months(today):
    assert today.diff_for_humans(today.subtract(months=2), True) == "2 months"
    assert today.diff_for_humans(today.add(months=2), True) == "2 months"


def test_diff_for_humans_absolute_years(today):
    assert today.diff_for_humans(today.subtract(years=1), True) == "1 year"
    assert today.diff_for_humans(today.add(years=1), True) == "1 year"


def test_subtraction():
    d = pendulum.date(2016, 7, 5)
    future_dt = date(2016, 7, 6)
    future = d.add(days=1)

    assert (future - d).total_seconds() == 86400
    assert (future_dt - d).total_seconds() == 86400
