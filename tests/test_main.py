from __future__ import annotations

import zoneinfo

from datetime import date
from datetime import datetime
from datetime import time

from dateutil import tz

import pendulum

from pendulum import _safe_timezone
from pendulum import timezone
from pendulum.tz.timezone import Timezone


def test_instance_with_naive_datetime_defaults_to_utc() -> None:
    now = pendulum.instance(datetime.now())
    assert now.timezone_name == "UTC"


def test_instance_with_aware_datetime() -> None:
    now = pendulum.instance(datetime.now(timezone("Europe/Paris")))
    assert now.timezone_name == "Europe/Paris"


def test_instance_with_aware_datetime_zoneinfo() -> None:
    now = pendulum.instance(datetime.now(zoneinfo.ZoneInfo("Europe/Paris")))
    assert now.timezone_name == "Europe/Paris"


def test_instance_with_aware_datetime_any_tzinfo() -> None:
    dt = datetime(2016, 8, 7, 12, 34, 56, tzinfo=tz.gettz("Europe/Paris"))
    now = pendulum.instance(dt)
    assert now.timezone_name == "+02:00"


def test_instance_with_aware_datetime_and_explicit_tz_converts() -> None:
    dt = datetime(2024, 9, 3, 13, 56, 35, tzinfo=timezone("Europe/Brussels"))
    now = pendulum.instance(dt, tz="EST")

    assert now.timezone_name == "EST"
    # 13:56 in Brussels (UTC+2) is 06:56 EST (UTC-5)
    assert (now.hour, now.minute, now.second) == (6, 56, 35)
    assert now == dt


def test_instance_with_pendulum_datetime_and_explicit_tz_converts() -> None:
    dt = pendulum.datetime(2024, 9, 3, 13, 56, 35, tz="Europe/Brussels")
    now = pendulum.instance(dt, tz="EST")

    assert now.timezone_name == "EST"
    assert (now.hour, now.minute, now.second) == (6, 56, 35)
    assert now == dt


def test_instance_with_naive_datetime_and_explicit_tz() -> None:
    now = pendulum.instance(datetime(2024, 9, 3, 13, 56, 35), tz="Europe/Paris")

    assert now.timezone_name == "Europe/Paris"
    assert (now.hour, now.minute, now.second) == (13, 56, 35)


def test_datetime_instance_with_explicit_tz_converts() -> None:
    dt = pendulum.datetime(2024, 9, 3, 13, 56, 35, tz="Europe/Brussels")
    converted = pendulum.DateTime.instance(dt, tz="America/New_York")

    assert converted.timezone_name == "America/New_York"
    # 13:56 in Brussels (UTC+2) is 07:56 in New York (UTC-4)
    assert (converted.hour, converted.minute, converted.second) == (7, 56, 35)
    assert converted == dt


def test_instance_with_date() -> None:
    dt = pendulum.instance(date(2022, 12, 23))

    assert isinstance(dt, pendulum.Date)


def test_instance_with_naive_time() -> None:
    dt = pendulum.instance(time(12, 34, 56, 123456))

    assert isinstance(dt, pendulum.Time)


def test_instance_with_aware_time() -> None:
    dt = pendulum.instance(time(12, 34, 56, 123456, tzinfo=timezone("Europe/Paris")))

    assert isinstance(dt, pendulum.Time)
    assert isinstance(dt.tzinfo, Timezone)
    assert dt.tzinfo.name == "Europe/Paris"


def test_safe_timezone_with_tzinfo_objects() -> None:
    tz = _safe_timezone(zoneinfo.ZoneInfo("Europe/Paris"))

    assert isinstance(tz, Timezone)
    assert tz.name == "Europe/Paris"
