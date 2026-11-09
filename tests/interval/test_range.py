from __future__ import annotations

import pytest

import pendulum

from pendulum.interval import Interval
from tests.conftest import assert_datetime


def test_range():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = Interval(dt1, dt2)
    r = list(p.range("days"))

    assert len(r) == 31
    assert_datetime(r[0], 2000, 1, 1, 12, 45, 37)
    assert_datetime(r[-1], 2000, 1, 31, 12, 45, 37)


def test_range_no_overflow():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 11, 45, 37)

    p = Interval(dt1, dt2)
    r = list(p.range("days"))

    assert len(r) == 30
    assert_datetime(r[0], 2000, 1, 1, 12, 45, 37)
    assert_datetime(r[-1], 2000, 1, 30, 12, 45, 37)


def test_range_inverted():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = Interval(dt2, dt1)
    r = list(p.range("days"))

    assert len(r) == 31
    assert_datetime(r[-1], 2000, 1, 1, 12, 45, 37)
    assert_datetime(r[0], 2000, 1, 31, 12, 45, 37)


def test_iter():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = Interval(dt1, dt2)
    i = 0
    for dt in p:
        assert isinstance(dt, pendulum.DateTime)
        i += 1

    assert i == 31


def test_contains():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = pendulum.interval(dt1, dt2)
    dt = pendulum.datetime(2000, 1, 7)
    assert dt in p


def test_not_contains():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = pendulum.interval(dt1, dt2)
    dt = pendulum.datetime(2000, 1, 1, 11, 45, 37)
    assert dt not in p


def test_contains_with_datetime():
    dt1 = pendulum.datetime(2000, 1, 1, 12, 45, 37)
    dt2 = pendulum.datetime(2000, 1, 31, 12, 45, 37)

    p = pendulum.interval(dt1, dt2)
    dt = pendulum.datetime(2000, 1, 7)
    assert dt in p


def test_range_months_overflow():
    dt1 = pendulum.datetime(2016, 1, 30, tz="America/Sao_Paulo")
    dt2 = dt1.add(months=4)

    p = pendulum.interval(dt1, dt2)
    r = list(p.range("months"))

    assert_datetime(r[0], 2016, 1, 30, 0, 0, 0)
    assert_datetime(r[-1], 2016, 5, 30, 0, 0, 0)


def test_range_with_dst():
    dt1 = pendulum.datetime(2016, 10, 14, tz="America/Sao_Paulo")
    dt2 = dt1.add(weeks=1)

    p = pendulum.interval(dt1, dt2)
    r = list(p.range("days"))

    assert_datetime(r[0], 2016, 10, 14, 0, 0, 0)
    assert_datetime(r[2], 2016, 10, 16, 1, 0, 0)
    assert_datetime(r[-1], 2016, 10, 21, 0, 0, 0)


def test_range_amount():
    dt1 = pendulum.datetime(2016, 10, 14, tz="America/Sao_Paulo")
    dt2 = dt1.add(weeks=1)

    p = pendulum.interval(dt1, dt2)
    r = list(p.range("days", 2))

    assert len(r) == 4
    assert_datetime(r[0], 2016, 10, 14, 0, 0, 0)
    assert_datetime(r[1], 2016, 10, 16, 1, 0, 0)
    assert_datetime(r[2], 2016, 10, 18, 0, 0, 0)
    assert_datetime(r[3], 2016, 10, 20, 0, 0, 0)


def test_range_zero_amount_raises():
    p = Interval(pendulum.datetime(2016, 1, 1), pendulum.datetime(2016, 2, 1))
    with pytest.raises(ValueError, match="positive integer"):
        list(p.range("days", 0))


def test_range_negative_amount_raises():
    p = Interval(pendulum.datetime(2016, 1, 1), pendulum.datetime(2016, 2, 1))
    with pytest.raises(ValueError, match="positive integer"):
        list(p.range("days", -1))
