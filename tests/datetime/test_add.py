from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_add_years_positive():
    assert pendulum.datetime(1975, 1, 1).add(years=1).year == 1976


def test_add_years_zero():
    assert pendulum.datetime(1975, 1, 1).add(years=0).year == 1975


def test_add_years_negative():
    assert pendulum.datetime(1975, 1, 1).add(years=-1).year == 1974


def test_add_months_positive():
    assert pendulum.datetime(1975, 12, 1).add(months=1).month == 1


def test_add_months_zero():
    assert pendulum.datetime(1975, 12, 1).add(months=0).month == 12


def test_add_months_negative():
    assert pendulum.datetime(1975, 12, 1).add(months=-1).month == 11


def test_add_month_with_overflow():
    assert pendulum.datetime(2012, 1, 31).add(months=1).month == 2


def test_add_days_positive():
    assert pendulum.datetime(1975, 5, 31).add(days=1).day == 1


def test_add_days_zero():
    assert pendulum.datetime(1975, 5, 31).add(days=0).day == 31


def test_add_days_negative():
    assert pendulum.datetime(1975, 5, 31).add(days=-1).day == 30


def test_add_weeks_positive():
    assert pendulum.datetime(1975, 5, 21).add(weeks=1).day == 28


def test_add_weeks_zero():
    assert pendulum.datetime(1975, 5, 21).add(weeks=0).day == 21


def test_add_weeks_negative():
    assert pendulum.datetime(1975, 5, 21).add(weeks=-1).day == 14


def test_add_hours_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=1).hour == 1


def test_add_hours_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=0).hour == 0


def test_add_hours_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=-1).hour == 23


def test_add_minutes_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=1).minute == 1


def test_add_minutes_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=0).minute == 0


def test_add_minutes_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=-1).minute == 59


def test_add_seconds_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=1).second == 1


def test_add_seconds_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=0).second == 0


def test_add_seconds_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=-1).second == 59


def test_add_timedelta():
    delta = timedelta(days=6, seconds=45, microseconds=123456)
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    d = d + delta
    assert d.day == 20
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_add_duration():
    duration = pendulum.duration(
        years=2, months=3, days=6, seconds=45, microseconds=123456
    )
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    d = d + duration
    assert d.year == 2017
    assert d.month == 6
    assert d.day == 20
    assert d.hour == 3
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_addition_invalid_type():
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d + 3

    with pytest.raises(TypeError):
        3 + d


def test_add_to_fixed_timezones():
    dt = pendulum.parse("2015-03-08T01:00:00-06:00")
    dt = dt.add(weeks=1)
    dt = dt.add(hours=1)

    assert_datetime(dt, 2015, 3, 15, 2, 0, 0)
    assert dt.timezone_name == "-06:00"
    assert dt.offset == -6 * 3600


def test_add_time_to_new_transition_skipped():
    dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 1, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 3, 31, 3, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = pendulum.datetime(2013, 3, 10, 1, 59, 59, 999999, tz="America/New_York")

    assert_datetime(dt, 2013, 3, 10, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 3, 10, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = pendulum.datetime(1957, 4, 28, 1, 59, 59, 999999, tz="America/New_York")

    assert_datetime(dt, 1957, 4, 28, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 1957, 4, 28, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()


def test_add_time_to_new_transition_skipped_big():
    dt = pendulum.datetime(2013, 3, 31, 1, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.add(weeks=1)

    assert_datetime(dt, 2013, 4, 7, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()


def test_add_time_to_new_transition_repeated():
    dt = pendulum.datetime(2013, 10, 27, 1, 59, 59, 999999, tz="Europe/Paris")
    dt = dt.add(hours=1)

    assert_datetime(dt, 2013, 10, 27, 2, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 10, 27, 2, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = pendulum.datetime(2013, 11, 3, 0, 59, 59, 999999, tz="America/New_York")
    dt = dt.add(hours=1)

    assert_datetime(dt, 2013, 11, 3, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 11, 3, 1, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()


def test_add_time_to_new_transition_repeated_big():
    dt = pendulum.datetime(2013, 10, 27, 1, tz="Europe/Paris")

    assert_datetime(dt, 2013, 10, 27, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.add(weeks=1)

    assert_datetime(dt, 2013, 11, 3, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()


def test_add_duration_across_transition():
    dt = pendulum.datetime(2017, 3, 11, 10, 45, tz="America/Los_Angeles")
    new = dt + pendulum.duration(hours=24)

    assert_datetime(new, 2017, 3, 12, 11, 45)


def test_add_duration_across_transition_days():
    dt = pendulum.datetime(2017, 3, 11, 10, 45, tz="America/Los_Angeles")
    new = dt + pendulum.duration(days=1)

    assert_datetime(new, 2017, 3, 12, 10, 45)

    dt = pendulum.datetime(2023, 11, 5, 0, 0, tz="America/Chicago")
    new = dt + pendulum.duration(days=1)

    assert_datetime(new, 2023, 11, 6, 0, 0)


def test_interval_over_midnight_tz():
    start = pendulum.datetime(2018, 2, 25, tz="Europe/Paris")
    end = start.add(hours=1)
    interval = end - start
    new_end = start + interval

    assert new_end == end


def test_add_rejects_bool():
    dt = pendulum.datetime(2020, 5, 15, 12, 30, 45)
    for key in ("years", "months", "weeks", "days", "hours", "minutes", "seconds", "microseconds"):
        with pytest.raises(TypeError, match=key):
            dt.add(**{key: True})
        with pytest.raises(TypeError, match=key):
            dt.add(**{key: False})
