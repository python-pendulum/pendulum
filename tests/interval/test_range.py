from __future__ import annotations

from itertools import islice

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


@pytest.mark.parametrize("factory", [pendulum.date, pendulum.datetime])
@pytest.mark.parametrize("absolute", [False, True])
@pytest.mark.parametrize(
    "start, end, unit, amount",
    [
        ((9999, 12, 30), (9999, 12, 31), "days", 1),
        ((1, 1, 2), (1, 1, 1), "days", 1),
        ((9999, 12, 31), (9999, 12, 31), "days", 1),
        ((1, 1, 1), (1, 1, 1), "days", 1),
        ((9999, 12, 29), (9999, 12, 31), "days", 2),
        ((1, 1, 3), (1, 1, 1), "days", 2),
        ((9999, 12, 24), (9999, 12, 31), "weeks", 1),
        ((1, 1, 8), (1, 1, 1), "weeks", 1),
        ((9999, 11, 30), (9999, 12, 30), "months", 1),
        ((1, 2, 1), (1, 1, 1), "months", 1),
        ((9998, 12, 31), (9999, 12, 31), "years", 1),
        ((2, 1, 1), (1, 1, 1), "years", 1),
    ],
)
def test_range_stops_at_final_endpoint(factory, absolute, start, end, unit, amount):
    start, end = factory(*start), factory(*end)
    interval = pendulum.interval(start, end, absolute=absolute)
    expected = [start] if start == end else [start, end]
    if absolute:
        expected.sort()

    assert list(interval.range(unit, amount)) == expected


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("unit", ["hours", "minutes", "seconds", "microseconds"])
def test_range_stops_at_final_datetime_endpoint(reverse, unit):
    if reverse:
        end = pendulum.datetime(1, 1, 1)
        start = end.add(**{unit: 1})
    else:
        end = pendulum.datetime(9999, 12, 31, 23, 59, 59, 999999)
        start = end.subtract(**{unit: 1})

    assert list(pendulum.interval(start, end).range(unit)) == [start, end]


@pytest.mark.parametrize("end_day", [1, 3])
def test_range_zero_amount(end_day):
    start = pendulum.date(2000, 1, 1)
    end = pendulum.date(2000, 1, end_day)

    assert list(islice(pendulum.interval(start, end).range("days", 0), 3)) == [
        start,
        start,
        start,
    ]


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("absolute", [False, True])
def test_range_amount_does_not_reach_endpoint(reverse, absolute):
    start, end = pendulum.date(2000, 1, 1), pendulum.date(2000, 1, 4)
    if reverse:
        start, end = end, start
    expected = [pendulum.date(2000, 1, 1), pendulum.date(2000, 1, 3)]
    if reverse and not absolute:
        expected = [pendulum.date(2000, 1, 4), pendulum.date(2000, 1, 2)]

    assert (
        list(pendulum.interval(start, end, absolute=absolute).range("days", 2))
        == expected
    )
