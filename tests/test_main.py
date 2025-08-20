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
