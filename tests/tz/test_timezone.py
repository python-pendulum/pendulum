from __future__ import annotations

import zoneinfo

from datetime import datetime
from datetime import timedelta

import pytest

import pendulum

from pendulum import timezone
from pendulum.tz import fixed_timezone
from pendulum.tz.exceptions import AmbiguousTime
from pendulum.tz.exceptions import NonExistingTime
from tests.conftest import assert_datetime


@pytest.fixture(autouse=True)
def setup():
    pendulum.tz._tz_cache = {}

    yield

    pendulum.tz._tz_cache = {}


def test_basic_convert():
    dt = datetime(2016, 6, 1, 12, 34, 56, 123456, fold=1)
    tz = timezone("Europe/Paris")
    dt = tz.convert(dt)

    assert dt.year == 2016
    assert dt.month == 6
    assert dt.day == 1
    assert dt.hour == 12
    assert dt.minute == 34
    assert dt.second == 56
    assert dt.microsecond == 123456
    assert dt.tzinfo.name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=7200)
    assert dt.tzinfo.dst(dt) == timedelta(seconds=3600)


def test_equality():
    assert timezone("Europe/Paris") == timezone("Europe/Paris")
    assert timezone("Europe/Paris") != timezone("Europe/Berlin")


def test_skipped_time_with_pre_rule():
    dt = datetime(2013, 3, 31, 2, 30, 45, 123456, fold=0)
    tz = timezone("Europe/Paris")
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 31
    assert dt.hour == 1
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=3600)
    assert dt.tzinfo.dst(dt) == timedelta()


def test_skipped_time_with_post_rule():
    dt = datetime(2013, 3, 31, 2, 30, 45, 123456, fold=1)
    tz = timezone("Europe/Paris")
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 31
    assert dt.hour == 3
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=7200)
    assert dt.tzinfo.dst(dt) == timedelta(seconds=3600)


def test_skipped_time_with_error():
    dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
    tz = timezone("Europe/Paris")
    with pytest.raises(NonExistingTime):
        tz.convert(dt, raise_on_unknown_times=True)


def test_repeated_time():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456, fold=1)
    tz = timezone("Europe/Paris")
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 10
    assert dt.day == 27
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=3600)
    assert dt.tzinfo.dst(dt) == timedelta()


def test_repeated_time_pre_rule():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456, fold=0)
    tz = timezone("Europe/Paris")
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 10
    assert dt.day == 27
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=7200)
    assert dt.tzinfo.dst(dt) == timedelta(seconds=3600)


def test_repeated_time_with_error():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
    tz = timezone("Europe/Paris")
    with pytest.raises(AmbiguousTime):
        tz.convert(dt, raise_on_unknown_times=True)


def test_pendulum_create_basic():
    dt = pendulum.datetime(2016, 6, 1, 12, 34, 56, 123456, tz="Europe/Paris")

    assert_datetime(dt, 2016, 6, 1, 12, 34, 56, 123456)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()


def test_pendulum_create_skipped():
    dt = pendulum.datetime(2013, 3, 31, 2, 30, 45, 123456, tz="Europe/Paris")

    assert isinstance(dt, pendulum.DateTime)
    assert_datetime(dt, 2013, 3, 31, 3, 30, 45, 123456)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=7200)
    assert dt.tzinfo.dst(dt) == timedelta(seconds=3600)


def test_pendulum_create_skipped_with_pre_rule():
    dt = pendulum.datetime(2013, 3, 31, 2, 30, 45, 123456, tz="Europe/Paris", fold=0)

    assert_datetime(dt, 2013, 3, 31, 1, 30, 45, 123456)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=3600)
    assert dt.tzinfo.dst(dt) == timedelta()


def test_pendulum_create_skipped_with_error():
    with pytest.raises(NonExistingTime):
        pendulum.datetime(
            2013,
            3,
            31,
            2,
            30,
            45,
            123456,
            tz="Europe/Paris",
            raise_on_unknown_times=True,
        )


def test_pendulum_create_repeated():
    dt = pendulum.datetime(2013, 10, 27, 2, 30, 45, 123456, tz="Europe/Paris")

    assert_datetime(dt, 2013, 10, 27, 2, 30, 45, 123456)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=3600)
    assert dt.tzinfo.dst(dt) == timedelta()


def test_pendulum_create_repeated_with_pre_rule():
    dt = pendulum.datetime(
        2013,
        10,
        27,
        2,
        30,
        45,
        123456,
        tz="Europe/Paris",
        fold=0,
    )

    assert_datetime(dt, 2013, 10, 27, 2, 30, 45, 123456)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.tzinfo.utcoffset(dt) == timedelta(seconds=7200)
    assert dt.tzinfo.dst(dt) == timedelta(seconds=3600)


def test_pendulum_create_repeated_with_error():
    with pytest.raises(AmbiguousTime):
        pendulum.datetime(
            2013,
            10,
            27,
            2,
            30,
            45,
            123456,
            tz="Europe/Paris",
            raise_on_unknown_times=True,
        )


def test_convert_accept_pendulum_instance():
    dt = pendulum.datetime(2016, 8, 7, 12, 53, 54)
    tz = timezone("Europe/Paris")
    new = tz.convert(dt)

    assert isinstance(new, pendulum.DateTime)
    assert_datetime(new, 2016, 8, 7, 14, 53, 54)


def test_utcoffset():
    tz = pendulum.timezone("America/Guayaquil")
    utcoffset = tz.utcoffset(pendulum.now("UTC"))
    assert utcoffset == timedelta(0, -18000)


def test_utcoffset_pre_transition():
    tz = pendulum.timezone("America/Chicago")
    utcoffset = tz.utcoffset(datetime(1883, 11, 18))
    assert utcoffset == timedelta(days=-1, seconds=65364)


def test_dst():
    tz = pendulum.timezone("Europe/Amsterdam")
    dst = tz.dst(datetime(1940, 7, 1))
    native_tz = zoneinfo.ZoneInfo("Europe/Amsterdam")

    assert dst == native_tz.dst(datetime(1940, 7, 1))


def test_short_timezones_should_not_modify_time():
    tz = pendulum.timezone("EST")
    dt = tz.datetime(2017, 6, 15, 14, 0, 0)

    assert dt.year == 2017
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0

    tz = pendulum.timezone("HST")
    dt = tz.datetime(2017, 6, 15, 14, 0, 0)

    assert dt.year == 2017
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0


def test_after_last_transition():
    tz = pendulum.timezone("Europe/Paris")
    dt = tz.datetime(2135, 6, 15, 14, 0, 0)

    assert dt.year == 2135
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0


@pytest.mark.skip(
    reason=(
        "zoneinfo does not currently support POSIX transition"
        " rules to go beyond the last fixed transition."
    )
)
def test_on_last_transition():
    tz = pendulum.timezone("Europe/Paris")
    dt = pendulum.naive(2037, 10, 25, 2, 30)
    dt = tz.convert(dt, dst_rule=pendulum.POST_TRANSITION)

    assert dt.year == 2037
    assert dt.month == 10
    assert dt.day == 25
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.utcoffset().total_seconds() == 3600

    dt = pendulum.naive(2037, 10, 25, 2, 30)
    dt = tz.convert(dt, dst_rule=pendulum.PRE_TRANSITION)

    assert dt.year == 2037
    assert dt.month == 10
    assert dt.day == 25
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.utcoffset().total_seconds() == 7200


def test_convert_fold_attribute_is_honored():
    tz = pendulum.timezone("US/Eastern")
    dt = datetime(2014, 11, 2, 1, 30)

    new = tz.convert(dt)
    assert new.strftime("%z") == "-0400"

    new = tz.convert(dt.replace(fold=1))
    assert new.strftime("%z") == "-0500"


def test_utcoffset_fold_attribute_is_honored():
    tz = pendulum.timezone("US/Eastern")
    dt = datetime(2014, 11, 2, 1, 30)

    offset = tz.utcoffset(dt)

    assert offset.total_seconds() == -4 * 3600

    offset = tz.utcoffset(dt.replace(fold=1))

    assert offset.total_seconds() == -5 * 3600


def test_dst_fold_attribute_is_honored():
    tz = pendulum.timezone("US/Eastern")
    dt = datetime(2014, 11, 2, 1, 30)

    offset = tz.dst(dt)

    assert offset.total_seconds() == 3600

    offset = tz.dst(dt.replace(fold=1))

    assert offset.total_seconds() == 0


def test_tzname_fold_attribute_is_honored():
    tz = pendulum.timezone("US/Eastern")
    dt = datetime(2014, 11, 2, 1, 30)

    name = tz.tzname(dt)

    assert name == "EDT"

    name = tz.tzname(dt.replace(fold=1))

    assert name == "EST"


def test_constructor_fold_attribute_is_honored():
    tz = pendulum.timezone("US/Eastern")
    dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz)

    assert dt.strftime("%z") == "-0400"

    dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz, fold=1)

    assert dt.strftime("%z") == "-0500"


def test_datetime():
    tz = timezone("Europe/Paris")

    dt = tz.datetime(2013, 3, 24, 1, 30)
    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 24
    assert dt.hour == 1
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0

    dt = tz.datetime(2013, 3, 31, 2, 30)
    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 31
    assert dt.hour == 3
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0


def test_fixed_timezone():
    tz = fixed_timezone(19800)
    tz2 = fixed_timezone(18000)
    dt = datetime(2016, 11, 26, tzinfo=tz)

    assert tz2.utcoffset(dt).total_seconds() == 18000
    assert tz2.dst(dt) == timedelta()


def test_fixed_equality():
    assert fixed_timezone(19800) == fixed_timezone(19800)
    assert fixed_timezone(19800) != fixed_timezone(19801)


def test_just_before_last_transition():
    tz = pendulum.timezone("Asia/Shanghai")
    dt = datetime(1991, 4, 20, 1, 49, 8, fold=0)
    dt = tz.convert(dt)

    epoch = datetime(1970, 1, 1, tzinfo=timezone("UTC"))
    expected = (dt - epoch).total_seconds()
    assert expected == 672079748.0


@pytest.mark.skip(
    reason=(
        "zoneinfo does not currently support POSIX transition"
        " rules to go beyond the last fixed transition."
    )
)
def test_timezones_are_extended():
    tz = pendulum.timezone("Europe/Paris")
    dt = tz.convert(pendulum.naive(2134, 2, 13, 1))

    assert_datetime(dt, 2134, 2, 13, 1)
    assert dt.utcoffset().total_seconds() == 3600
    assert dt.dst() == timedelta()

    dt = tz.convert(pendulum.naive(2134, 3, 28, 2, 30))

    assert_datetime(dt, 2134, 3, 28, 3, 30)
    assert dt.utcoffset().total_seconds() == 7200
    assert dt.dst() == timedelta(seconds=3600)

    dt = tz.convert(pendulum.naive(2134, 7, 11, 2, 30))

    assert_datetime(dt, 2134, 7, 11, 2, 30)
    assert dt.utcoffset().total_seconds() == 7200
    assert dt.dst() == timedelta(seconds=3600)

    dt = tz.convert(pendulum.naive(2134, 10, 31, 2, 30, fold=0))

    assert_datetime(dt, 2134, 10, 31, 2, 30)
    assert dt.utcoffset().total_seconds() == 7200
    assert dt.dst() == timedelta(seconds=3600)

    dt = tz.convert(pendulum.naive(2134, 10, 31, 2, 30))

    assert_datetime(dt, 2134, 10, 31, 2, 30)
    assert dt.utcoffset().total_seconds() == 3600
    assert dt.dst() == timedelta()


def test_repr():
    tz = timezone("Europe/Paris")

    assert repr(tz) == "Timezone('Europe/Paris')"
