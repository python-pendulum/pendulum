from __future__ import annotations

import zoneinfo

from datetime import datetime

import pendulum

from tests.conftest import assert_datetime


def test_equal_to_true():
    d1 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d2 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d3 = datetime(2000, 1, 1, 1, 2, 3, tzinfo=pendulum.UTC)

    assert d2 == d1
    assert d3 == d1


def test_equal_to_false():
    d1 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d2 = pendulum.datetime(2000, 1, 2, 1, 2, 3)
    d3 = datetime(2000, 1, 2, 1, 2, 3, tzinfo=pendulum.UTC)

    assert d2 != d1
    assert d3 != d1


def test_equal_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, 9, 0, 0, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=pendulum.timezone("America/Toronto"))

    assert d2 == d1
    assert d3 == d1


def test_equal_with_timezone_false():
    d1 = pendulum.datetime(2000, 1, 1, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.timezone("America/Toronto"))

    assert d2 != d1
    assert d3 == d1


def test_not_equal_to_true():
    d1 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d2 = pendulum.datetime(2000, 1, 2, 1, 2, 3)
    d3 = datetime(2000, 1, 2, 1, 2, 3, tzinfo=pendulum.UTC)

    assert d2 != d1
    assert d3 != d1


def test_not_equal_to_false():
    d1 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d2 = pendulum.datetime(2000, 1, 1, 1, 2, 3)
    d3 = datetime(2000, 1, 1, 1, 2, 3, tzinfo=pendulum.UTC)

    assert d2 == d1
    assert d3 == d1


def test_not_equal_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.timezone("America/Toronto"))

    assert d2 != d1
    assert d3 == d1


def test_not_equal_to_none():
    d1 = pendulum.datetime(2000, 1, 1, 1, 2, 3)

    assert d1 is not None


def test_greater_than_true():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(1999, 12, 31)
    d3 = datetime(1999, 12, 31, tzinfo=pendulum.UTC)

    assert d1 > d2
    assert d1 > d3


def test_greater_than_false():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 2)
    d3 = datetime(2000, 1, 2, tzinfo=pendulum.UTC)

    assert not d1 > d2
    assert not d1 > d3


def test_greater_than_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, 8, 59, 59, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, 8, 59, 59, tzinfo=zoneinfo.ZoneInfo("America/Vancouver"))

    assert d1 > d2
    assert d1 > d3


def test_greater_than_with_timezone_false():
    d1 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, 9, 0, 1, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, 9, 0, 1, tzinfo=zoneinfo.ZoneInfo("America/Vancouver"))

    assert not d1 > d2
    assert not d1 > d3


def test_greater_than_or_equal_true():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(1999, 12, 31)
    d3 = datetime(1999, 12, 31, tzinfo=pendulum.UTC)

    assert d1 >= d2
    assert d1 >= d3


def test_greater_than_or_equal_true_equal():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 1)
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.UTC)

    assert d1 >= d2
    assert d1 >= d3


def test_greater_than_or_equal_false():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 2)
    d3 = datetime(2000, 1, 2, tzinfo=pendulum.UTC)

    assert not d1 >= d2
    assert not d1 >= d3


def test_greater_than_or_equal_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, 8, 59, 59, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, 8, 59, 59, tzinfo=zoneinfo.ZoneInfo("America/Vancouver"))

    assert d1 >= d2
    assert d1 >= d3


def test_greater_than_or_equal_with_timezone_false():
    d1 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d2 = pendulum.datetime(2000, 1, 1, 9, 0, 1, tz="America/Vancouver")
    d3 = datetime(2000, 1, 1, 9, 0, 1, tzinfo=zoneinfo.ZoneInfo("America/Vancouver"))

    assert not d1 >= d2
    assert not d1 >= d3


def test_less_than_true():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 2)
    d3 = datetime(2000, 1, 2, tzinfo=pendulum.UTC)

    assert d1 < d2
    assert d1 < d3


def test_less_than_false():
    d1 = pendulum.datetime(2000, 1, 2)
    d2 = pendulum.datetime(2000, 1, 1)
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.UTC)

    assert not d1 < d2
    assert not d1 < d3


def test_less_than_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, 8, 59, 59, tz="America/Vancouver")
    d2 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d3 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Toronto"))

    assert d1 < d2
    assert d1 < d3


def test_less_than_with_timezone_false():
    d1 = pendulum.datetime(2000, 1, 1, 9, 0, 1, tz="America/Vancouver")
    d2 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d3 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Toronto"))

    assert not d1 < d2
    assert not d1 < d3


def test_less_than_or_equal_true():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 2)
    d3 = datetime(2000, 1, 2, tzinfo=pendulum.UTC)

    assert d1 <= d2
    assert d1 <= d3


def test_less_than_or_equal_true_equal():
    d1 = pendulum.datetime(2000, 1, 1)
    d2 = pendulum.datetime(2000, 1, 1)
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.UTC)

    assert d1 <= d2
    assert d1 <= d3


def test_less_than_or_equal_false():
    d1 = pendulum.datetime(2000, 1, 2)
    d2 = pendulum.datetime(2000, 1, 1)
    d3 = datetime(2000, 1, 1, tzinfo=pendulum.UTC)

    assert not d1 <= d2
    assert not d1 <= d3


def test_less_than_or_equal_with_timezone_true():
    d1 = pendulum.datetime(2000, 1, 1, 8, 59, 59, tz="America/Vancouver")
    d2 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d3 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Toronto"))

    assert d1 <= d2
    assert d1 <= d3


def test_less_than_or_equal_with_timezone_false():
    d1 = pendulum.datetime(2000, 1, 1, 9, 0, 1, tz="America/Vancouver")
    d2 = pendulum.datetime(2000, 1, 1, 12, 0, 0, tz="America/Toronto")
    d3 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo("America/Toronto"))

    assert not d1 <= d2
    assert not d1 <= d3


def test_is_anniversary():
    with pendulum.travel_to(pendulum.now()):
        d = pendulum.now()
        an_anniversary = d.subtract(years=1)
        assert an_anniversary.is_anniversary()
        not_an_anniversary = d.subtract(days=1)
        assert not not_an_anniversary.is_anniversary()
        also_not_an_anniversary = d.add(days=2)
        assert not also_not_an_anniversary.is_anniversary()

    d1 = pendulum.datetime(1987, 4, 23)
    d2 = pendulum.datetime(2014, 9, 26)
    d3 = pendulum.datetime(2014, 4, 23)
    assert not d2.is_anniversary(d1)
    assert d3.is_anniversary(d1)


def test_is_birthday():  # backward compatibility
    with pendulum.travel_to(pendulum.now()):
        d = pendulum.now()
        an_anniversary = d.subtract(years=1)
        assert an_anniversary.is_birthday()
        not_an_anniversary = d.subtract(days=1)
        assert not not_an_anniversary.is_birthday()
        also_not_an_anniversary = d.add(days=2)
        assert not also_not_an_anniversary.is_birthday()

    d1 = pendulum.datetime(1987, 4, 23)
    d2 = pendulum.datetime(2014, 9, 26)
    d3 = pendulum.datetime(2014, 4, 23)
    assert not d2.is_birthday(d1)
    assert d3.is_birthday(d1)


def test_closest():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = pendulum.datetime(2015, 5, 28, 11, 0, 0)
    dt2 = pendulum.datetime(2015, 5, 28, 14, 0, 0)
    closest = instance.closest(dt1, dt2)
    assert closest == dt1

    closest = instance.closest(dt2, dt1)
    assert closest == dt1

    dts = [
        pendulum.datetime(2015, 5, 28, 16, 0, 0) + pendulum.duration(hours=x)
        for x in range(4)
    ]
    closest = instance.closest(*dts)
    assert closest == dts[0]

    closest = instance.closest(*(dts[::-1]))
    assert closest == dts[0]


def test_closest_with_datetime():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = datetime(2015, 5, 28, 11, 0, 0)
    dt2 = datetime(2015, 5, 28, 14, 0, 0)
    closest = instance.closest(dt1, dt2)
    assert_datetime(closest, 2015, 5, 28, 11, 0, 0)

    dts = [
        pendulum.datetime(2015, 5, 28, 16, 0, 0) + pendulum.duration(hours=x)
        for x in range(4)
    ]
    closest = instance.closest(dt1, dt2, *dts)

    assert_datetime(closest, 2015, 5, 28, 11, 0, 0)


def test_closest_with_equals():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt2 = pendulum.datetime(2015, 5, 28, 14, 0, 0)
    closest = instance.closest(dt1, dt2)
    assert closest == dt1


def test_farthest():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = pendulum.datetime(2015, 5, 28, 11, 0, 0)
    dt2 = pendulum.datetime(2015, 5, 28, 14, 0, 0)
    farthest = instance.farthest(dt1, dt2)
    assert farthest == dt2

    farthest = instance.farthest(dt2, dt1)
    assert farthest == dt2

    dts = [
        pendulum.datetime(2015, 5, 28, 16, 0, 0) + pendulum.duration(hours=x)
        for x in range(4)
    ]
    farthest = instance.farthest(*dts)
    assert farthest == dts[-1]

    farthest = instance.farthest(*(dts[::-1]))
    assert farthest == dts[-1]

    f = pendulum.datetime(2010, 1, 1, 0, 0, 0)
    assert f == instance.farthest(f, *(dts))


def test_farthest_with_datetime():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = datetime(2015, 5, 28, 11, 0, 0, tzinfo=pendulum.UTC)
    dt2 = datetime(2015, 5, 28, 14, 0, 0, tzinfo=pendulum.UTC)
    farthest = instance.farthest(dt1, dt2)
    assert_datetime(farthest, 2015, 5, 28, 14, 0, 0)

    dts = [
        pendulum.datetime(2015, 5, 28, 16, 0, 0) + pendulum.duration(hours=x)
        for x in range(4)
    ]
    farthest = instance.farthest(dt1, dt2, *dts)

    assert_datetime(farthest, 2015, 5, 28, 19, 0, 0)


def test_farthest_with_equals():
    instance = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt1 = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt2 = pendulum.datetime(2015, 5, 28, 14, 0, 0)
    farthest = instance.farthest(dt1, dt2)
    assert farthest == dt2

    dts = [
        pendulum.datetime(2015, 5, 28, 16, 0, 0) + pendulum.duration(hours=x)
        for x in range(4)
    ]
    farthest = instance.farthest(dt1, dt2, *dts)
    assert farthest == dts[-1]


def test_is_same_day():
    dt1 = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt2 = pendulum.datetime(2015, 5, 29, 12, 0, 0)
    dt3 = pendulum.datetime(2015, 5, 28, 12, 0, 0)
    dt4 = datetime(2015, 5, 28, 12, 0, 0, tzinfo=pendulum.UTC)
    dt5 = datetime(2015, 5, 29, 12, 0, 0, tzinfo=pendulum.UTC)

    assert not dt1.is_same_day(dt2)
    assert dt1.is_same_day(dt3)
    assert dt1.is_same_day(dt4)
    assert not dt1.is_same_day(dt5)


def test_comparison_to_unsupported():
    dt1 = pendulum.now()

    assert dt1 != "test"
    assert dt1 not in ["test"]
