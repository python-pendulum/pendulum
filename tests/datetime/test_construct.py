from __future__ import annotations

import os

from datetime import datetime

import pytest

import pendulum

from pendulum import DateTime
from pendulum import timezone
from pendulum.utils._compat import PYPY
from tests.conftest import assert_datetime


if not PYPY:
    import time_machine
else:
    time_machine = None


@pytest.fixture(autouse=True)
def _setup():
    yield

    if os.getenv("TZ"):
        del os.environ["TZ"]


def test_creates_an_instance_default_to_utcnow():
    now = pendulum.now("UTC")
    p = pendulum.datetime(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )
    assert now.timezone_name == p.timezone_name

    assert_datetime(p, now.year, now.month, now.day, now.hour, now.minute, now.second)


def test_setting_timezone():
    tz = "Australia/Brisbane"
    dtz = timezone(tz)
    dt = datetime.utcnow()
    offset = dtz.convert(dt).utcoffset().total_seconds() / 3600

    p = pendulum.datetime(dt.year, dt.month, dt.day, tz=dtz)
    assert p.timezone_name == tz
    assert p.offset_hours == int(offset)


def test_setting_timezone_with_string():
    tz = "Australia/Brisbane"
    dtz = timezone(tz)
    dt = datetime.utcnow()
    offset = dtz.convert(dt).utcoffset().total_seconds() / 3600

    p = pendulum.datetime(dt.year, dt.month, dt.day, tz=tz)
    assert p.timezone_name == tz
    assert p.offset_hours == int(offset)


def test_today():
    today = pendulum.today()
    assert isinstance(today, DateTime)


def test_tomorrow():
    now = pendulum.now().start_of("day")
    tomorrow = pendulum.tomorrow()
    assert isinstance(tomorrow, DateTime)
    assert now.diff(tomorrow).in_days() == 1


def test_yesterday():
    now = pendulum.now().start_of("day")
    yesterday = pendulum.yesterday()

    assert isinstance(yesterday, DateTime)
    assert now.diff(yesterday, False).in_days() == -1


def test_now():
    now = pendulum.now("America/Toronto")
    in_paris = pendulum.now("Europe/Paris")

    assert now.hour != in_paris.hour


if time_machine:

    @time_machine.travel("2016-03-27 00:30:00Z", tick=False)
    def test_now_dst_off():
        utc = pendulum.now("UTC")
        in_paris = pendulum.now("Europe/Paris")
        in_paris_from_utc = utc.in_tz("Europe/Paris")
        assert in_paris.hour == 1
        assert not in_paris.is_dst()
        assert in_paris.isoformat() == in_paris_from_utc.isoformat()

    @time_machine.travel("2016-03-27 01:30:00Z", tick=False)
    def test_now_dst_transitioning_on():
        utc = pendulum.now("UTC")
        in_paris = pendulum.now("Europe/Paris")
        in_paris_from_utc = utc.in_tz("Europe/Paris")
        assert in_paris.hour == 3
        assert in_paris.is_dst()
        assert in_paris.isoformat() == in_paris_from_utc.isoformat()

    @time_machine.travel("2016-10-30 00:30:00Z", tick=False)
    def test_now_dst_on():
        utc = pendulum.now("UTC")
        in_paris = pendulum.now("Europe/Paris")
        in_paris_from_utc = utc.in_tz("Europe/Paris")
        assert in_paris.hour == 2
        assert in_paris.is_dst()
        assert in_paris.isoformat() == in_paris_from_utc.isoformat()

    @time_machine.travel("2016-10-30 01:30:00Z", tick=False)
    def test_now_dst_transitioning_off():
        utc = pendulum.now("UTC")
        in_paris = pendulum.now("Europe/Paris")
        in_paris_from_utc = utc.in_tz("Europe/Paris")
        assert in_paris.hour == 2
        assert not in_paris.is_dst()
        assert in_paris.isoformat() == in_paris_from_utc.isoformat()


def test_now_with_fixed_offset():
    now = pendulum.now(6)

    assert now.timezone_name == "+06:00"


def test_create_with_no_transition_timezone():
    dt = pendulum.now("Etc/UTC")

    assert dt.timezone_name == "Etc/UTC"


def test_create_maintains_microseconds():
    d = pendulum.datetime(2016, 11, 12, 2, 9, 39, 594000, tz="America/Panama")
    assert_datetime(d, 2016, 11, 12, 2, 9, 39, 594000)

    d = pendulum.datetime(2316, 11, 12, 2, 9, 39, 857, tz="America/Panama")
    assert_datetime(d, 2316, 11, 12, 2, 9, 39, 857)


def test_second_inaccuracy_on_past_datetimes():
    dt = pendulum.datetime(1901, 12, 13, 0, 0, 0, 555555, tz="US/Central")

    assert_datetime(dt, 1901, 12, 13, 0, 0, 0, 555555)


def test_local():
    local = pendulum.local(2018, 2, 2, 12, 34, 56, 123456)

    assert_datetime(local, 2018, 2, 2, 12, 34, 56, 123456)
    assert local.timezone_name == "America/Toronto"
