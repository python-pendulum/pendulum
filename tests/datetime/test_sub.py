from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_sub_years_positive():
    assert pendulum.datetime(1975, 1, 1).subtract(years=1).year == 1974


def test_sub_years_zero():
    assert pendulum.datetime(1975, 1, 1).subtract(years=0).year == 1975


def test_sub_years_negative():
    assert pendulum.datetime(1975, 1, 1).subtract(years=-1).year == 1976


def test_sub_months_positive():
    assert pendulum.datetime(1975, 12, 1).subtract(months=1).month == 11


def test_sub_months_zero():
    assert pendulum.datetime(1975, 12, 1).subtract(months=0).month == 12


def test_sub_months_negative():
    assert pendulum.datetime(1975, 12, 1).subtract(months=-1).month == 1


def test_sub_days_positive():
    assert pendulum.datetime(1975, 5, 31).subtract(days=1).day == 30


def test_sub_days_zero():
    assert pendulum.datetime(1975, 5, 31).subtract(days=0).day == 31


def test_sub_days_negative():
    assert pendulum.datetime(1975, 5, 31).subtract(days=-1).day == 1


def test_sub_weeks_positive():
    assert pendulum.datetime(1975, 5, 21).subtract(weeks=1).day == 14


def test_sub_weeks_zero():
    assert pendulum.datetime(1975, 5, 21).subtract(weeks=0).day == 21


def test_sub_weeks_negative():
    assert pendulum.datetime(1975, 5, 21).subtract(weeks=-1).day == 28


def test_sub_hours_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(hours=1).hour == 23


def test_sub_hours_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(hours=0).hour == 0


def test_sub_hours_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(hours=-1).hour == 1


def test_sub_minutes_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(minutes=1).minute == 59


def test_sub_minutes_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(minutes=0).minute == 0


def test_sub_minutes_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(minutes=-1).minute == 1


def test_sub_seconds_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(seconds=1).second == 59


def test_sub_seconds_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(seconds=0).second == 0


def test_sub_seconds_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).subtract(seconds=-1).second == 1


def test_subtract_timedelta():
    delta = timedelta(days=6, seconds=16, microseconds=654321)
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 777777)

    d = d - delta
    assert d.day == 8
    assert d.minute == 11
    assert d.second == 59
    assert d.microsecond == 123456


def test_subtract_duration():
    duration = pendulum.duration(
        years=2, months=3, days=6, seconds=16, microseconds=654321
    )
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 777777)

    d = d - duration
    assert d.year == 2012
    assert d.month == 12
    assert d.day == 8
    assert d.hour == 3
    assert d.minute == 11
    assert d.second == 59
    assert d.microsecond == 123456


def test_subtract_duration_days_across_dst_matches_method():
    # `- duration(days=...)` must be calendar-aware like `.subtract(days=...)`
    # and `+ duration(days=-...)`, not fold days into absolute seconds.
    d = pendulum.datetime(2013, 4, 2, tz="Europe/Paris")  # spring-forward is 2013-03-31

    assert (d - pendulum.duration(days=3)) == d.subtract(days=3)
    assert (d - pendulum.duration(days=3)) == (d + pendulum.duration(days=-3))
    assert (d - pendulum.duration(weeks=1)) == d.subtract(weeks=1)

    # round-trip stability across a transition
    dt = pendulum.datetime(2023, 3, 12, 5, 0, tz="America/New_York")
    one = pendulum.duration(days=1)
    assert (dt - one) + one == dt


def test_subtract_time_to_new_transition_skipped():
    dt = pendulum.datetime(2013, 3, 31, 3, 0, 0, 0, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 3, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.subtract(microseconds=1)

    assert_datetime(dt, 2013, 3, 31, 1, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = pendulum.datetime(2013, 3, 10, 3, 0, 0, 0, tz="America/New_York")

    assert_datetime(dt, 2013, 3, 10, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = dt.subtract(microseconds=1)

    assert_datetime(dt, 2013, 3, 10, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = pendulum.datetime(1957, 4, 28, 3, 0, 0, 0, tz="America/New_York")

    assert_datetime(dt, 1957, 4, 28, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = dt.subtract(microseconds=1)

    assert_datetime(dt, 1957, 4, 28, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()


def test_subtract_time_to_new_transition_skipped_big():
    dt = pendulum.datetime(2013, 3, 31, 3, 0, 0, 0, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 3, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.subtract(days=1)

    assert_datetime(dt, 2013, 3, 30, 3, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()


def test_subtract_time_to_new_transition_repeated():
    dt = pendulum.datetime(2013, 10, 27, 2, 0, 0, 0, tz="Europe/Paris")

    assert_datetime(dt, 2013, 10, 27, 2, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.subtract(microseconds=1)

    assert_datetime(dt, 2013, 10, 27, 2, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = pendulum.datetime(2013, 11, 3, 1, 0, 0, 0, tz="America/New_York")

    assert_datetime(dt, 2013, 11, 3, 1, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = dt.subtract(microseconds=1)

    assert_datetime(dt, 2013, 11, 3, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()


def test_subtract_time_to_new_transition_repeated_big():
    dt = pendulum.datetime(2013, 10, 27, 2, 0, 0, 0, tz="Europe/Paris")

    assert_datetime(dt, 2013, 10, 27, 2, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.subtract(days=1)

    assert_datetime(dt, 2013, 10, 26, 2, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()


def test_subtract_invalid_type():
    d = pendulum.datetime(1975, 5, 21, 0, 0, 0)

    with pytest.raises(TypeError):
        d - "ab"

    with pytest.raises(TypeError):
        "ab" - d


def test_subtract_negative_over_dls_transitioning_off():
    just_before_dls_ends = pendulum.datetime(
        2019, 11, 3, 1, 30, tz="US/Pacific", fold=0
    )
    plus_10_hours = just_before_dls_ends + timedelta(hours=10)
    minus_neg_10_hours = just_before_dls_ends - timedelta(hours=-10)

    # 1:30-0700 becomes 10:30-0800
    assert plus_10_hours.hour == 10
    assert minus_neg_10_hours.hour == 10
    assert just_before_dls_ends.is_dst()
    assert not plus_10_hours.is_dst()
    assert not minus_neg_10_hours.is_dst()
