from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from zoneinfo import ZoneInfo

import pytest

from dateutil import tz

import pendulum

from tests.conftest import assert_datetime


def test_in_timezone():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_timezone("Europe/Paris")
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_in_tz():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_tz("Europe/Paris")
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_astimezone():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.astimezone(pendulum.timezone("Europe/Paris"))
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


class CustomDateTime(pendulum.DateTime):
    pass


@pytest.mark.parametrize("datetime_class", [pendulum.DateTime, CustomDateTime])
@pytest.mark.parametrize(
    "target",
    [
        pytest.param(tz.gettz("Etc/GMT+6"), id="dateutil-fixed-zone"),
        pytest.param(tz.gettz("Europe/Paris"), id="dateutil-dst-zone"),
        pytest.param(tz.tzoffset("offset", 19800), id="dateutil-offset"),
        pytest.param(timezone(timedelta(hours=5, minutes=30)), id="builtin"),
        pytest.param(ZoneInfo("Europe/Paris"), id="zoneinfo"),
        pytest.param(pendulum.timezone("Europe/Paris"), id="pendulum"),
        pytest.param(None, id="local"),
    ],
)
@pytest.mark.parametrize(
    "source",
    [
        datetime(2024, 1, 15, 18, 15, 34, 123456, tzinfo=timezone.utc),
        datetime(2024, 7, 15, 18, 15, 34, 123456, tzinfo=timezone.utc),
        datetime(2024, 10, 27, 0, 30, tzinfo=timezone.utc),
        datetime(2024, 10, 27, 1, 30, tzinfo=timezone.utc),
        datetime(2024, 10, 27, 2, 30, tzinfo=ZoneInfo("Europe/Paris"), fold=1),
        datetime(2024, 1, 15, 18, 15, 34, 123456),
    ],
)
def test_astimezone_matches_datetime(datetime_class, target, source):
    value = datetime_class(
        source.year,
        source.month,
        source.day,
        source.hour,
        source.minute,
        source.second,
        source.microsecond,
        tzinfo=source.tzinfo,
        fold=source.fold,
    )

    expected = source.astimezone(target)
    actual = value.astimezone(target)

    assert type(actual) is datetime_class
    assert actual.tzinfo == expected.tzinfo
    assert actual.isoformat() == expected.isoformat()
    assert actual.timestamp() == expected.timestamp()
    assert actual.fold == expected.fold
