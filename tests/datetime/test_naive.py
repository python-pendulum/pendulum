from __future__ import annotations

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_naive():
    dt = pendulum.naive(2018, 2, 2, 12, 34, 56, 123456)

    assert_datetime(dt, 2018, 2, 2, 12, 34, 56, 123456)
    assert dt.tzinfo is None
    assert dt.timezone is None
    assert dt.timezone_name is None


def test_naive_add():
    dt = pendulum.naive(2013, 3, 31, 1, 30)
    new = dt.add(hours=1)

    assert_datetime(new, 2013, 3, 31, 2, 30)


def test_naive_subtract():
    dt = pendulum.naive(2013, 3, 31, 1, 30)
    new = dt.subtract(hours=1)

    assert_datetime(new, 2013, 3, 31, 0, 30)


def test_naive_in_timezone():
    dt = pendulum.naive(2013, 3, 31, 1, 30)
    new = dt.in_timezone("Europe/Paris")

    assert_datetime(new, 2013, 3, 31, 1, 30)
    assert new.timezone_name == "Europe/Paris"


def test_naive_in_timezone_dst():
    dt = pendulum.naive(2013, 3, 31, 2, 30)
    new = dt.in_timezone("Europe/Paris")

    assert_datetime(new, 2013, 3, 31, 3, 30)
    assert new.timezone_name == "Europe/Paris"


def test_add():
    dt = pendulum.naive(2013, 3, 31, 2, 30)
    new = dt.add(days=3)

    assert_datetime(new, 2013, 4, 3, 2, 30)


def test_subtract():
    dt = pendulum.naive(2013, 3, 31, 2, 30)
    new = dt.subtract(days=3)

    assert_datetime(new, 2013, 3, 28, 2, 30)


def test_to_strings():
    dt = pendulum.naive(2013, 3, 31, 2, 30)

    assert dt.isoformat() == "2013-03-31T02:30:00"
    assert dt.to_iso8601_string() == "2013-03-31T02:30:00"
    assert dt.to_rfc3339_string() == "2013-03-31T02:30:00"
    assert dt.to_atom_string() == "2013-03-31T02:30:00"
    assert dt.to_cookie_string() == "Sunday, 31-Mar-2013 02:30:00 "


def test_naive_method():
    dt = pendulum.datetime(2018, 2, 2, 12, 34, 56, 123456)
    dt = dt.naive()

    assert_datetime(dt, 2018, 2, 2, 12, 34, 56, 123456)
    assert dt.tzinfo is None
    assert dt.timezone is None
    assert dt.timezone_name is None


@pytest.mark.parametrize("fold", [0, 1])
@pytest.mark.parametrize(
    "tz, year, month, day, hour, minute",
    [
        ("America/New_York", 2024, 11, 3, 1, 30),
        ("Australia/Lord_Howe", 2024, 4, 7, 1, 45),
    ],
)
def test_naive_method_preserves_fold(tz, year, month, day, hour, minute, fold):
    dt = pendulum.datetime(year, month, day, hour, minute, 12, 345678, tz=tz, fold=fold)

    naive = dt.naive()

    assert isinstance(naive, pendulum.DateTime)
    assert_datetime(naive, year, month, day, hour, minute, 12, 345678)
    assert naive.tzinfo is None
    assert naive.fold == fold
    assert naive.replace(tzinfo=dt.tzinfo).timestamp() == dt.timestamp()
    assert naive.naive().fold == fold
