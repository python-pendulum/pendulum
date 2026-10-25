from __future__ import annotations

from datetime import time

import pendulum

from pendulum import Time


def test_diff_in_hours_positive():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(hours=2).add(seconds=3672)).in_hours() == 3


def test_diff_in_hours_negative_with_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(hours=2).add(seconds=3600), False).in_hours() == -1


def test_diff_in_hours_negative_no_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(hours=2).add(seconds=3600)).in_hours() == 1


def test_diff_in_hours_vs_default_now():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(hours=2).diff().in_hours() == 2


def test_diff_in_hours_ensure_is_truncated():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(hours=2).add(seconds=5401)).in_hours() == 3


def test_diff_in_minutes_positive():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(hours=1).add(minutes=2)).in_minutes() == 62


def test_diff_in_minutes_positive_big():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(hours=25).add(minutes=2)).in_minutes() == 62


def test_diff_in_minutes_negative_with_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(hours=1).add(minutes=2), False).in_minutes() == -58


def test_diff_in_minutes_negative_no_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(hours=1).add(minutes=2)).in_minutes() == 58


def test_diff_in_minutes_vs_default_now():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(hours=1).diff().in_minutes() == 60


def test_diff_in_minutes_ensure_is_truncated():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(minutes=1).add(seconds=59)).in_minutes() == 1


def test_diff_in_seconds_positive():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(minutes=1).add(seconds=2)).in_seconds() == 62


def test_diff_in_seconds_positive_big():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(hours=2).add(seconds=2)).in_seconds() == 7202


def test_diff_in_seconds_negative_with_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(minutes=1).add(seconds=2), False).in_seconds() == -58


def test_diff_in_seconds_negative_no_sign():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.subtract(minutes=1).add(seconds=2)).in_seconds() == 58


def test_diff_in_seconds_vs_default_now():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(hours=1).diff().in_seconds() == 3600


def test_diff_in_seconds_ensure_is_truncated():
    dt = Time(12, 34, 56)
    assert dt.diff(dt.add(seconds=1.9)).in_seconds() == 1


def test_diff_includes_microseconds():
    dt = Time(12, 0, 0, 500000)
    diff = dt.diff(Time(12, 0, 1))

    assert diff.total_seconds() == 0.5
    assert diff.microseconds == 500000
    assert diff.in_seconds() == 0


def test_diff_includes_microseconds_negative_with_sign():
    dt = Time(12, 0, 1)
    diff = dt.diff(Time(12, 0, 0, 250000), False)

    assert diff.total_seconds() == -0.75
    assert diff.microseconds == -750000


def test_diff_includes_microseconds_within_the_same_second():
    dt = Time(12, 0, 0, 1)
    assert dt.diff(Time(12, 0, 0, 999999)).total_seconds() == 0.999998


def test_diff_includes_microseconds_of_native_time():
    dt = Time(12, 0, 0)
    assert dt.diff(time(12, 0, 0, 750000)).total_seconds() == 0.75


def test_diff_min_and_max():
    assert Time.min.diff(Time.max).total_seconds() == 86399.999999


def test_diff_for_humans_now_and_second():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans() == "a few seconds ago"


def test_diff_for_humans_now_and_seconds():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(seconds=2).diff_for_humans() == "a few seconds ago"


def test_diff_for_humans_now_and_nearly_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(seconds=59).diff_for_humans() == "59 seconds ago"


def test_diff_for_humans_now_and_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(minutes=1).diff_for_humans() == "1 minute ago"


def test_diff_for_humans_now_and_minutes():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(minutes=2).diff_for_humans() == "2 minutes ago"


def test_diff_for_humans_now_and_nearly_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(minutes=59).diff_for_humans() == "59 minutes ago"


def test_diff_for_humans_now_and_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(hours=1).diff_for_humans() == "1 hour ago"


def test_diff_for_humans_now_and_hours():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.subtract(hours=2).diff_for_humans() == "2 hours ago"


def test_diff_for_humans_now_and_future_second():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.add(seconds=1).diff_for_humans() == "in a few seconds"


def test_diff_for_humans_now_and_future_seconds():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.add(seconds=2).diff_for_humans() == "in a few seconds"


def test_diff_for_humans_now_and_nearly_future_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(seconds=59).diff_for_humans() == "in 59 seconds"


def test_diff_for_humans_now_and_future_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(minutes=1).diff_for_humans() == "in 1 minute"


def test_diff_for_humans_now_and_future_minutes():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(minutes=2).diff_for_humans() == "in 2 minutes"


def test_diff_for_humans_now_and_nearly_future_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(minutes=59).diff_for_humans() == "in 59 minutes"


def test_diff_for_humans_now_and_future_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(hours=1).diff_for_humans() == "in 1 hour"


def test_diff_for_humans_now_and_future_hours():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56), freeze=True):
        now = pendulum.now().time()

        assert now.add(hours=2).diff_for_humans() == "in 2 hours"


def test_diff_for_humans_other_and_second():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(seconds=1)) == "a few seconds before"


def test_diff_for_humans_other_and_seconds():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(seconds=2)) == "a few seconds before"


def test_diff_for_humans_other_and_nearly_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(seconds=59)) == "59 seconds before"


def test_diff_for_humans_other_and_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(minutes=1)) == "1 minute before"


def test_diff_for_humans_other_and_minutes():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(minutes=2)) == "2 minutes before"


def test_diff_for_humans_other_and_nearly_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(minutes=59)) == "59 minutes before"


def test_diff_for_humans_other_and_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(hours=1)) == "1 hour before"


def test_diff_for_humans_other_and_hours():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(hours=2)) == "2 hours before"


def test_diff_for_humans_other_and_future_second():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(seconds=1)) == "a few seconds after"


def test_diff_for_humans_other_and_future_seconds():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(seconds=2)) == "a few seconds after"


def test_diff_for_humans_other_and_nearly_future_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(seconds=59)) == "59 seconds after"


def test_diff_for_humans_other_and_future_minute():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(minutes=1)) == "1 minute after"


def test_diff_for_humans_other_and_future_minutes():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(minutes=2)) == "2 minutes after"


def test_diff_for_humans_other_and_nearly_future_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(minutes=59)) == "59 minutes after"


def test_diff_for_humans_other_and_future_hour():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(hours=1)) == "1 hour after"


def test_diff_for_humans_other_and_future_hours():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(hours=2)) == "2 hours after"


def test_diff_for_humans_absolute_seconds():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(seconds=59), True) == "59 seconds"
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(seconds=59), True) == "59 seconds"


def test_diff_for_humans_absolute_minutes():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(minutes=30), True) == "30 minutes"
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(minutes=30), True) == "30 minutes"


def test_diff_for_humans_absolute_hours():
    with pendulum.travel_to(pendulum.today().at(12, 34, 56)):
        now = pendulum.now().time()

        assert now.diff_for_humans(now.subtract(hours=3), True) == "3 hours"
        now = pendulum.now().time()

        assert now.diff_for_humans(now.add(hours=3), True) == "3 hours"
