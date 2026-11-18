from __future__ import annotations

from datetime import datetime

import pendulum

from tests.conftest import assert_datetime


def test_fluid_year_setter():
    d = pendulum.now()
    new = d.set(year=1995)
    assert isinstance(new, datetime)
    assert new.year == 1995
    assert d.year != new.year


def test_fluid_month_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(month=11)
    assert isinstance(new, datetime)
    assert new.month == 11
    assert d.month == 7


def test_fluid_day_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(day=9)
    assert isinstance(new, datetime)
    assert new.day == 9
    assert d.day == 2


def test_fluid_hour_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(hour=5)
    assert isinstance(new, datetime)
    assert new.hour == 5
    assert d.hour == 0


def test_fluid_minute_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(minute=32)
    assert isinstance(new, datetime)
    assert new.minute == 32
    assert d.minute == 41


def test_fluid_second_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(second=49)
    assert isinstance(new, datetime)
    assert new.second == 49
    assert d.second == 20


def test_fluid_microsecond_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20, 123456)
    new = d.set(microsecond=987654)
    assert isinstance(new, datetime)
    assert new.microsecond == 987654
    assert d.microsecond == 123456


def test_fluid_setter_keeps_timezone():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20, 123456, tz="Europe/Paris")
    new = d.set(microsecond=987654)
    assert_datetime(new, 2016, 7, 2, 0, 41, 20, 987654)


def test_fluid_timezone_setter():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.set(tz="Europe/Paris")
    assert isinstance(new, datetime)
    assert new.timezone_name == "Europe/Paris"
    assert new.tzinfo.name == "Europe/Paris"


def test_fluid_on():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.on(1995, 11, 9)
    assert isinstance(new, datetime)
    assert new.year == 1995
    assert new.month == 11
    assert new.day == 9
    assert d.year == 2016
    assert d.month == 7
    assert d.day == 2


def test_fluid_on_with_transition():
    d = pendulum.datetime(2013, 3, 31, 0, 0, 0, 0, tz="Europe/Paris")
    new = d.on(2013, 4, 1)
    assert isinstance(new, datetime)
    assert new.year == 2013
    assert new.month == 4
    assert new.day == 1
    assert new.offset == 7200
    assert d.year == 2013
    assert d.month == 3
    assert d.day == 31
    assert d.offset == 3600


def test_fluid_at():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.at(5, 32, 49, 123456)
    assert isinstance(new, datetime)
    assert new.hour == 5
    assert new.minute == 32
    assert new.second == 49
    assert new.microsecond == 123456
    assert d.hour == 0
    assert d.minute == 41
    assert d.second == 20
    assert d.microsecond == 0


def test_fluid_at_partial():
    d = pendulum.datetime(2016, 7, 2, 0, 41, 20)
    new = d.at(10)

    assert_datetime(new, 2016, 7, 2, 10, 0, 0, 0)

    new = d.at(10, 30)

    assert_datetime(new, 2016, 7, 2, 10, 30, 0, 0)

    new = d.at(10, 30, 45)

    assert_datetime(new, 2016, 7, 2, 10, 30, 45, 0)


def test_fluid_at_with_transition():
    d = pendulum.datetime(2013, 3, 31, 0, 0, 0, 0, tz="Europe/Paris")
    new = d.at(2, 30, 0)
    assert isinstance(new, datetime)
    assert new.hour == 3
    assert new.minute == 30
    assert new.second == 0


def test_replace_tzinfo_dst_off():
    d = pendulum.datetime(2016, 3, 27, 0, 30)  # 30 min before DST turning on
    new = d.replace(tzinfo=pendulum.timezone("Europe/Paris"))

    assert_datetime(new, 2016, 3, 27, 0, 30)
    assert not new.is_dst()
    assert new.offset == 3600
    assert new.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_transitioning_on():
    d = pendulum.datetime(2016, 3, 27, 1, 30)  # In middle of turning on
    new = d.replace(tzinfo=pendulum.timezone("Europe/Paris"))

    assert_datetime(new, 2016, 3, 27, 1, 30)
    assert not new.is_dst()
    assert new.offset == 3600
    assert new.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_on():
    d = pendulum.datetime(2016, 10, 30, 0, 30)  # 30 min before DST turning off
    new = d.replace(tzinfo=pendulum.timezone("Europe/Paris"))

    assert_datetime(new, 2016, 10, 30, 0, 30)
    assert new.is_dst()
    assert new.offset == 7200
    assert new.timezone_name == "Europe/Paris"


def test_replace_tzinfo_dst_transitioning_off():
    d = pendulum.datetime(2016, 10, 30, 1, 30)  # In the middle of turning off
    new = d.replace(tzinfo=pendulum.timezone("Europe/Paris"))

    assert_datetime(new, 2016, 10, 30, 1, 30)
    assert new.is_dst()
    assert new.offset == 7200
    assert new.timezone_name == "Europe/Paris"


def test_set_rejects_bool():
    import pytest

    dt = pendulum.datetime(2020, 5, 15, 12, 30, 45)
    for key in ("year", "month", "day", "hour", "minute", "second", "microsecond"):
        with pytest.raises(TypeError, match=key):
            dt.set(**{key: True})
        with pytest.raises(TypeError, match=key):
            dt.set(**{key: False})
