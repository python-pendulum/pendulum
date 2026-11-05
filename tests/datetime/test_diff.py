from __future__ import annotations

from datetime import datetime

import pytest

import pendulum


def test_diff_in_years_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_years() == 1


def test_diff_in_years_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_years() == -1


def test_diff_in_years_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_years() == 1


def test_diff_in_years_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(years=1).diff().in_years() == 1


def test_diff_in_years_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(years=1).add(months=7)).in_years() == 1


def test_diff_in_months_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(years=1).add(months=1)).in_months() == 13


def test_diff_in_months_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1).add(months=1), False).in_months() == -11


def test_diff_in_months_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1).add(months=1)).in_months() == 11


def test_diff_in_months_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(years=1).diff().in_months() == 12


def test_diff_in_months_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(months=1).add(days=16)).in_months() == 1


def test_diff_in_days_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_days() == 366


def test_diff_in_days_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_days() == -365


def test_diff_in_days_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_days() == 365


def test_diff_in_days_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=1).diff().in_days() == 7


def test_diff_in_days_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(days=1).add(hours=13)).in_days() == 1


def test_diff_in_weeks_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(years=1)).in_weeks() == 52


def test_diff_in_weeks_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1), False).in_weeks() == -52


def test_diff_in_weeks_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(years=1)).in_weeks() == 52


def test_diff_in_weeks_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=1).diff().in_weeks() == 1


def test_diff_in_weeks_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks() == 0


def test_diff_in_hours_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(days=1).add(hours=2)).in_hours() == 26


def test_diff_in_hours_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(days=1).add(hours=2), False).in_hours() == -22


def test_diff_in_hours_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(days=1).add(hours=2)).in_hours() == 22


def test_diff_in_hours_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 15), freeze=True):
        assert pendulum.now().subtract(days=2).diff().in_hours() == 48


def test_diff_in_hours_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(hours=1).add(minutes=31)).in_hours() == 1


def test_diff_in_minutes_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(hours=1).add(minutes=2)).in_minutes() == 62


def test_diff_in_minutes_positive_big():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(hours=25).add(minutes=2)).in_minutes() == 1502


def test_diff_in_minutes_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(hours=1).add(minutes=2), False).in_minutes() == -58


def test_diff_in_minutes_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(hours=1).add(minutes=2)).in_minutes() == 58


def test_diff_in_minutes_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(hours=1).diff().in_minutes() == 60


def test_diff_in_minutes_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(minutes=1).add(seconds=59)).in_minutes() == 1


def test_diff_in_seconds_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(minutes=1).add(seconds=2)).in_seconds() == 62


def test_diff_in_seconds_positive_big():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(hours=2).add(seconds=2)).in_seconds() == 7202


def test_diff_in_seconds_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(minutes=1).add(seconds=2), False).in_seconds() == -58


def test_diff_in_seconds_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.subtract(minutes=1).add(seconds=2)).in_seconds() == 58


def test_diff_in_seconds_vs_default_now():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(hours=1).diff().in_seconds() == 3600


def test_diff_in_seconds_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert dt.diff(dt.add(seconds=1.9)).in_seconds() == 1


def test_diff_in_seconds_with_timezones():
    dt_ottawa = pendulum.datetime(2000, 1, 1, 13, tz="America/Toronto")
    dt_vancouver = pendulum.datetime(2000, 1, 1, 13, tz="America/Vancouver")
    assert dt_ottawa.diff(dt_vancouver).in_seconds() == 3 * 60 * 60


def test_diff_naive_with_naive_stdlib_datetime():
    # A naive DateTime diffed against a naive stdlib datetime should not
    # force the latter to UTC, which used to make it offset-aware and raise
    # "can't compare offset-naive and offset-aware datetimes". See #880.
    dt = pendulum.naive(2016, 7, 5, 12, 0, 0)
    other = datetime(2016, 7, 5, 13, 0, 0)

    assert dt.diff(other).in_seconds() == 3600
    assert dt.diff(other, False).in_seconds() == 3600
    assert other.tzinfo is None


def test_diff_for_humans_now_and_second():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().diff_for_humans() == "a few seconds ago"


def test_diff_for_humans_now_and_second_with_timezone():
    van_now = pendulum.now("America/Vancouver")
    here_now = van_now.in_timezone(pendulum.now().timezone)

    with pendulum.travel_to(here_now, freeze=True):
        assert here_now.diff_for_humans() == "a few seconds ago"


def test_diff_for_humans_now_and_seconds():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().subtract(seconds=2).diff_for_humans() == "a few seconds ago"
        )


def test_diff_for_humans_now_and_nearly_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(seconds=59).diff_for_humans() == "59 seconds ago"


def test_diff_for_humans_now_and_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(minutes=1).diff_for_humans() == "1 minute ago"


def test_diff_for_humans_now_and_minutes():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(minutes=2).diff_for_humans() == "2 minutes ago"


def test_diff_for_humans_now_and_nearly_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(minutes=59).diff_for_humans() == "59 minutes ago"


def test_diff_for_humans_now_and_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(hours=1).diff_for_humans() == "1 hour ago"


def test_diff_for_humans_now_and_hours():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(hours=2).diff_for_humans() == "2 hours ago"


def test_diff_for_humans_now_and_nearly_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(hours=23).diff_for_humans() == "23 hours ago"


def test_diff_for_humans_now_and_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(days=1).diff_for_humans() == "1 day ago"


def test_diff_for_humans_now_and_days():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(days=2).diff_for_humans() == "2 days ago"


def test_diff_for_humans_now_and_nearly_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(days=6).diff_for_humans() == "6 days ago"


def test_diff_for_humans_now_and_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=1).diff_for_humans() == "1 week ago"


def test_diff_for_humans_now_and_weeks():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=2).diff_for_humans() == "2 weeks ago"


def test_diff_for_humans_now_and_nearly_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=3).diff_for_humans() == "3 weeks ago"


def test_diff_for_humans_now_and_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(weeks=4).diff_for_humans() == "4 weeks ago"
        assert pendulum.now().subtract(months=1).diff_for_humans() == "1 month ago"


def test_diff_for_humans_now_and_months():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(months=2).diff_for_humans() == "2 months ago"


def test_diff_for_humans_now_and_nearly_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(months=11).diff_for_humans() == "11 months ago"


def test_diff_for_humans_now_and_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(years=1).diff_for_humans() == "1 year ago"


def test_diff_for_humans_now_and_years():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().subtract(years=2).diff_for_humans() == "2 years ago"


def test_diff_for_humans_now_and_future_second():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(seconds=1).diff_for_humans() == "in a few seconds"


def test_diff_for_humans_now_and_future_seconds():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(seconds=2).diff_for_humans() == "in a few seconds"


def test_diff_for_humans_now_and_nearly_future_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(seconds=59).diff_for_humans() == "in 59 seconds"


def test_diff_for_humans_now_and_future_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(minutes=1).diff_for_humans() == "in 1 minute"


def test_diff_for_humans_now_and_future_minutes():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(minutes=2).diff_for_humans() == "in 2 minutes"


def test_diff_for_humans_now_and_nearly_future_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(minutes=59).diff_for_humans() == "in 59 minutes"


def test_diff_for_humans_now_and_future_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(hours=1).diff_for_humans() == "in 1 hour"


def test_diff_for_humans_now_and_future_hours():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(hours=2).diff_for_humans() == "in 2 hours"


def test_diff_for_humans_now_and_nearly_future_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(hours=23).diff_for_humans() == "in 23 hours"


def test_diff_for_humans_now_and_future_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(days=1).diff_for_humans() == "in 1 day"


def test_diff_for_humans_now_and_future_days():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(days=2).diff_for_humans() == "in 2 days"


def test_diff_for_humans_now_and_nearly_future_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(days=6).diff_for_humans() == "in 6 days"


def test_diff_for_humans_now_and_future_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(weeks=1).diff_for_humans() == "in 1 week"


def test_diff_for_humans_now_and_future_weeks():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(weeks=2).diff_for_humans() == "in 2 weeks"


def test_diff_for_humans_now_and_nearly_future_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(weeks=3).diff_for_humans() == "in 3 weeks"


def test_diff_for_humans_now_and_future_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(weeks=4).diff_for_humans() == "in 4 weeks"
        assert pendulum.now().add(months=1).diff_for_humans() == "in 1 month"


def test_diff_for_humans_now_and_future_months():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(months=2).diff_for_humans() == "in 2 months"


def test_diff_for_humans_now_and_nearly_future_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(months=11).diff_for_humans() == "in 11 months"


def test_diff_for_humans_now_and_future_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(years=1).diff_for_humans() == "in 1 year"


def test_diff_for_humans_now_and_future_years():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert pendulum.now().add(years=2).diff_for_humans() == "in 2 years"


def test_diff_for_humans_other_and_second():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(seconds=1))
            == "a few seconds before"
        )


def test_diff_for_humans_other_and_seconds():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(seconds=2))
            == "a few seconds before"
        )


def test_diff_for_humans_other_and_nearly_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(seconds=59))
            == "59 seconds before"
        )


def test_diff_for_humans_other_and_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(minutes=1))
            == "1 minute before"
        )


def test_diff_for_humans_other_and_minutes():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(minutes=2))
            == "2 minutes before"
        )


def test_diff_for_humans_other_and_nearly_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(minutes=59))
            == "59 minutes before"
        )


def test_diff_for_humans_other_and_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(hours=1))
            == "1 hour before"
        )


def test_diff_for_humans_other_and_hours():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(hours=2))
            == "2 hours before"
        )


def test_diff_for_humans_other_and_nearly_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(hours=23))
            == "23 hours before"
        )


def test_diff_for_humans_other_and_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(days=1)) == "1 day before"
        )


def test_diff_for_humans_other_and_days():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(days=2))
            == "2 days before"
        )


def test_diff_for_humans_other_and_nearly_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(days=6))
            == "6 days before"
        )


def test_diff_for_humans_other_and_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(weeks=1))
            == "1 week before"
        )


def test_diff_for_humans_other_and_weeks():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(weeks=2))
            == "2 weeks before"
        )


def test_diff_for_humans_other_and_nearly_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(weeks=3))
            == "3 weeks before"
        )


def test_diff_for_humans_other_and_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(weeks=4))
            == "4 weeks before"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(months=1))
            == "1 month before"
        )


def test_diff_for_humans_other_and_months():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(months=2))
            == "2 months before"
        )


def test_diff_for_humans_other_and_nearly_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(months=11))
            == "11 months before"
        )


def test_diff_for_humans_other_and_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(years=1))
            == "1 year before"
        )


def test_diff_for_humans_other_and_years():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(years=2))
            == "2 years before"
        )


def test_diff_for_humans_other_and_future_second():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(seconds=1))
            == "a few seconds after"
        )


def test_diff_for_humans_other_and_future_seconds():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(seconds=2))
            == "a few seconds after"
        )


def test_diff_for_humans_other_and_nearly_future_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(seconds=59))
            == "59 seconds after"
        )


def test_diff_for_humans_other_and_future_minute():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(minutes=1))
            == "1 minute after"
        )


def test_diff_for_humans_other_and_future_minutes():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(minutes=2))
            == "2 minutes after"
        )


def test_diff_for_humans_other_and_nearly_future_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(minutes=59))
            == "59 minutes after"
        )


def test_diff_for_humans_other_and_future_hour():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(hours=1))
            == "1 hour after"
        )


def test_diff_for_humans_other_and_future_hours():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(hours=2))
            == "2 hours after"
        )


def test_diff_for_humans_other_and_nearly_future_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(hours=23))
            == "23 hours after"
        )


def test_diff_for_humans_other_and_future_day():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(days=1))
            == "1 day after"
        )


def test_diff_for_humans_other_and_future_days():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(days=2))
            == "2 days after"
        )


def test_diff_for_humans_other_and_nearly_future_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(days=6))
            == "6 days after"
        )


def test_diff_for_humans_other_and_future_week():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(weeks=1))
            == "1 week after"
        )


def test_diff_for_humans_other_and_future_weeks():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(weeks=2))
            == "2 weeks after"
        )


def test_diff_for_humans_other_and_nearly_future_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(weeks=3))
            == "3 weeks after"
        )


def test_diff_for_humans_other_and_future_month():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(weeks=4))
            == "4 weeks after"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(months=1))
            == "1 month after"
        )


def test_diff_for_humans_other_and_future_months():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(months=2))
            == "2 months after"
        )


def test_diff_for_humans_other_and_nearly_future_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(months=11))
            == "11 months after"
        )


def test_diff_for_humans_other_and_future_year():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(years=1))
            == "1 year after"
        )


def test_diff_for_humans_other_and_future_years():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(years=2))
            == "2 years after"
        )


def test_diff_for_humans_absolute_seconds():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(seconds=59), True)
            == "59 seconds"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(seconds=59), True)
            == "59 seconds"
        )


def test_diff_for_humans_absolute_minutes():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(minutes=30), True)
            == "30 minutes"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(minutes=30), True)
            == "30 minutes"
        )


def test_diff_for_humans_absolute_hours():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(hours=3), True)
            == "3 hours"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(hours=3), True)
            == "3 hours"
        )


def test_diff_for_humans_absolute_days():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(days=2), True)
            == "2 days"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(days=2), True) == "2 days"
        )


def test_diff_for_humans_absolute_weeks():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(weeks=2), True)
            == "2 weeks"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(weeks=2), True)
            == "2 weeks"
        )


def test_diff_for_humans_absolute_months():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(months=2), True)
            == "2 months"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(months=2), True)
            == "2 months"
        )


def test_diff_for_humans_absolute_years():
    with pendulum.travel_to(pendulum.datetime(2012, 1, 1, 1, 2, 3), freeze=True):
        assert (
            pendulum.now().diff_for_humans(pendulum.now().subtract(years=1), True)
            == "1 year"
        )
        assert (
            pendulum.now().diff_for_humans(pendulum.now().add(years=1), True)
            == "1 year"
        )


def test_diff_for_humans_accuracy():
    now = pendulum.now("utc")

    with pendulum.travel_to(now.add(microseconds=200), freeze=True):
        assert now.add(years=1).diff_for_humans(absolute=True) == "1 year"
        assert now.add(months=11).diff_for_humans(absolute=True) == "11 months"
        assert now.add(days=27).diff_for_humans(absolute=True) == "4 weeks"
        assert now.add(years=1, months=3).diff_for_humans(absolute=True) == "1 year"
        assert now.add(years=1, months=8).diff_for_humans(absolute=True) == "2 years"

    # DST
    now = pendulum.datetime(2017, 3, 7, tz="America/Toronto")
    with pendulum.travel_to(now, freeze=True):
        assert now.add(days=6).diff_for_humans(absolute=True) == "6 days"


def test_subtraction():
    d = pendulum.naive(2016, 7, 5, 12, 32, 25, 0)
    future_dt = datetime(2016, 7, 5, 13, 32, 25, 0)
    future = d.add(hours=1)

    assert (future - d).total_seconds() == 3600
    assert (future_dt - d).total_seconds() == 3600


def test_subtraction_aware_naive():
    dt = pendulum.datetime(2016, 7, 5, 12, 32, 25, 0)
    future_dt = datetime(2016, 7, 5, 13, 32, 25, 0)

    with pytest.raises(TypeError):
        future_dt - dt

    future_dt = pendulum.naive(2016, 7, 5, 13, 32, 25, 0)

    with pytest.raises(TypeError):
        future_dt - dt


def test_subtraction_with_timezone():
    dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz="Europe/Paris")
    post = dt.add(microseconds=1)

    assert (post - dt).total_seconds() == 1e-06

    dt = pendulum.datetime(
        2013,
        10,
        27,
        2,
        59,
        59,
        999999,
        tz="Europe/Paris",
        fold=0,
    )
    post = dt.add(microseconds=1)

    assert (post - dt).total_seconds() == 1e-06
