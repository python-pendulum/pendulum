from __future__ import annotations

import zoneinfo

from datetime import datetime

import pytest

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


@pytest.mark.parametrize("method", ["closest", "farthest"])
@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_closest_and_farthest_with_naive_datetimes(method, native, reverse):
    instance = pendulum.naive(2026, 10, 20, 12, 34, 56, 123456)
    near = instance.subtract(microseconds=1)
    far = instance.add(microseconds=2)
    candidates = [near, far]
    if native:
        candidates = [
            datetime(
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond,
            )
            for dt in candidates
        ]
    if reverse:
        candidates.reverse()

    result = getattr(instance, method)(*candidates)

    assert result == (near if method == "closest" else far)
    assert type(result) is pendulum.DateTime
    assert result.tzinfo is None


@pytest.mark.parametrize("method", ["closest", "farthest"])
def test_closest_and_farthest_with_naive_single_candidate(method):
    instance = pendulum.naive(2026, 10, 20)

    assert getattr(instance, method)(instance) == instance


@pytest.mark.parametrize("method", ["closest", "farthest"])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("tz", [None, "UTC"])
def test_closest_and_farthest_with_ties(method, reverse, tz):
    instance = pendulum.datetime(2026, 10, 20, 12, tz=tz)
    before = instance.subtract(hours=1)
    after = instance.add(hours=1)
    candidates = [before, after]
    if reverse:
        candidates.reverse()

    result = getattr(instance, method)(*candidates)

    assert result == candidates[0]
    assert result.tzinfo == instance.tzinfo


@pytest.mark.parametrize("method", ["closest", "farthest"])
def test_closest_and_farthest_with_naive_subclass(method):
    class CustomDateTime(pendulum.DateTime):
        pass

    instance = CustomDateTime(2026, 10, 20, 12)
    candidates = [datetime(2026, 10, 20, 11), datetime(2026, 10, 20, 14)]

    result = getattr(instance, method)(*candidates)

    assert type(result) is CustomDateTime
    assert result.hour == (11 if method == "closest" else 14)
    assert result.tzinfo is None


@pytest.mark.parametrize("method", ["closest", "farthest"])
@pytest.mark.parametrize("tz", [None, "UTC", "Europe/Paris"])
def test_closest_and_farthest_without_candidates(method, tz):
    instance = pendulum.datetime(2026, 10, 20, tz=tz)

    with pytest.raises(ValueError):
        getattr(instance, method)()


@pytest.mark.parametrize("method", ["closest", "farthest"])
def test_closest_and_farthest_with_naive_reference_and_aware_candidate(method):
    instance = pendulum.naive(2026, 10, 20)
    candidate = pendulum.datetime(2026, 10, 21)

    with pytest.raises(TypeError, match="offset-naive and offset-aware"):
        getattr(instance, method)(candidate)


@pytest.mark.parametrize("method", ["closest", "farthest"])
def test_closest_and_farthest_aware_reference_keeps_naive_candidate_default(method):
    instance = pendulum.datetime(2026, 10, 20, 12, tz="Europe/Paris")
    naive = datetime(2026, 10, 20, 10)
    aware = pendulum.datetime(2026, 10, 20, 13, tz="Europe/Paris")

    result = getattr(instance, method)(naive, aware)

    assert result == (pendulum.instance(naive) if method == "closest" else aware)
    assert result.timezone_name == ("UTC" if method == "closest" else "Europe/Paris")


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
