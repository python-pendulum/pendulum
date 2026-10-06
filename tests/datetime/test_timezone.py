from __future__ import annotations

from datetime import datetime

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


def test_astimezone_with_tzinfo_doing_arithmetic_in_fromutc():
    # dateutil's tzoffset.fromutc() adds its offset to the datetime it's given
    cest = tz.tzoffset("CEST", 7200)
    d = pendulum.datetime(2024, 7, 1, 12)

    d = d.astimezone(cest)
    assert isinstance(d, pendulum.DateTime)
    assert d.tzinfo is cest
    assert_datetime(d, 2024, 7, 1, 14)


@pytest.mark.parametrize("fold, hour", [(0, 0), (1, 1)])
def test_astimezone_respects_fold(fold, hour):
    d = pendulum.datetime(2024, 10, 27, 2, 30, tz="Europe/Paris", fold=fold)

    d = d.astimezone(pendulum.UTC)
    assert d == datetime(2024, 10, 27, hour, 30, tzinfo=pendulum.UTC)
