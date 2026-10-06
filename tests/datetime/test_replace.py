from __future__ import annotations

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_replace_tzinfo_dst_off():
    utc = pendulum.datetime(2016, 3, 27, 0, 30)  # 30 min before DST turning on
    in_paris = utc.in_tz("Europe/Paris")

    assert_datetime(in_paris, 2016, 3, 27, 1, 30, 0)

    in_paris = in_paris.replace(second=1)

    assert_datetime(in_paris, 2016, 3, 27, 1, 30, 1)
    assert not in_paris.is_dst()
    assert in_paris.offset == 3600
    assert in_paris.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_transitioning_on():
    utc = pendulum.datetime(2016, 3, 27, 1, 30)  # In middle of turning on
    in_paris = utc.in_tz("Europe/Paris")

    assert_datetime(in_paris, 2016, 3, 27, 3, 30, 0)

    in_paris = in_paris.replace(second=1)

    assert_datetime(in_paris, 2016, 3, 27, 3, 30, 1)
    assert in_paris.is_dst()
    assert in_paris.offset == 7200
    assert in_paris.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_on():
    utc = pendulum.datetime(2016, 10, 30, 0, 30)  # 30 min before DST turning off
    in_paris = utc.in_tz("Europe/Paris")

    assert_datetime(in_paris, 2016, 10, 30, 2, 30, 0)

    in_paris = in_paris.replace(second=1)

    assert_datetime(in_paris, 2016, 10, 30, 2, 30, 1)
    assert in_paris.is_dst()
    assert in_paris.offset == 7200
    assert in_paris.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_transitioning_off():
    utc = pendulum.datetime(2016, 10, 30, 1, 30)  # In the middle of turning off
    in_paris = utc.in_tz("Europe/Paris")

    assert_datetime(in_paris, 2016, 10, 30, 2, 30, 0)

    in_paris = in_paris.replace(second=1)

    assert_datetime(in_paris, 2016, 10, 30, 2, 30, 1)
    assert not in_paris.is_dst()
    assert in_paris.offset == 3600
    assert in_paris.timezone_name == "Europe/Paris"


def test_replace_rejects_bool():
    dt = pendulum.datetime(2020, 5, 15, 12, 30, 45)
    for key in ("year", "month", "day", "hour", "minute", "second", "microsecond", "fold"):
        with pytest.raises(TypeError, match=key):
            dt.replace(**{key: True})
        with pytest.raises(TypeError, match=key):
            dt.replace(**{key: False})


def test_replace_tzinfo_true_still_allowed():
    # tzinfo=True is the documented sentinel for keeping the current timezone
    dt = pendulum.datetime(2020, 5, 15, 12, 30, 45, tz="UTC")
    replaced = dt.replace(tzinfo=True)
    assert replaced.timezone_name == dt.timezone_name
