from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_add_years_positive():
    assert pendulum.datetime(1975, 1, 1).add(years=1).year == 1976


def test_add_years_zero():
    assert pendulum.datetime(1975, 1, 1).add(years=0).year == 1975


def test_add_years_negative():
    assert pendulum.datetime(1975, 1, 1).add(years=-1).year == 1974


def test_add_months_positive():
    assert pendulum.datetime(1975, 12, 1).add(months=1).month == 1


def test_add_months_zero():
    assert pendulum.datetime(1975, 12, 1).add(months=0).month == 12


def test_add_months_negative():
    assert pendulum.datetime(1975, 12, 1).add(months=-1).month == 11


def test_add_month_with_overflow():
    assert pendulum.datetime(2012, 1, 31).add(months=1).month == 2


def test_add_days_positive():
    assert pendulum.datetime(1975, 5, 31).add(days=1).day == 1


def test_add_days_zero():
    assert pendulum.datetime(1975, 5, 31).add(days=0).day == 31


def test_add_days_negative():
    assert pendulum.datetime(1975, 5, 31).add(days=-1).day == 30


def test_add_weeks_positive():
    assert pendulum.datetime(1975, 5, 21).add(weeks=1).day == 28


def test_add_weeks_zero():
    assert pendulum.datetime(1975, 5, 21).add(weeks=0).day == 21


def test_add_weeks_negative():
    assert pendulum.datetime(1975, 5, 21).add(weeks=-1).day == 14


def test_add_hours_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=1).hour == 1


def test_add_hours_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=0).hour == 0


def test_add_hours_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(hours=-1).hour == 23


def test_add_minutes_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=1).minute == 1


def test_add_minutes_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=0).minute == 0


def test_add_minutes_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(minutes=-1).minute == 59


def test_add_seconds_positive():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=1).second == 1


def test_add_seconds_zero():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=0).second == 0


def test_add_seconds_negative():
    assert pendulum.datetime(1975, 5, 21, 0, 0, 0).add(seconds=-1).second == 59


def test_add_timedelta():
    delta = timedelta(days=6, seconds=45, microseconds=123456)
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    d = d + delta
    assert d.day == 20
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_add_timedelta_does_not_depend_on_caller_name():
    def astimezone(d):
        return d + timedelta(hours=24)

    d = pendulum.datetime(2013, 3, 30, 12, tz="Europe/Paris")

    assert_datetime(astimezone(d), 2013, 3, 31, 13)


def test_add_duration():
    duration = pendulum.duration(
        years=2, months=3, days=6, seconds=45, microseconds=123456
    )
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    d = d + duration
    assert d.year == 2017
    assert d.month == 6
    assert d.day == 20
    assert d.hour == 3
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_addition_invalid_type():
    d = pendulum.datetime(2015, 3, 14, 3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d + 3

    with pytest.raises(TypeError):
        3 + d


def test_add_to_fixed_timezones():
    dt = pendulum.parse("2015-03-08T01:00:00-06:00")
    dt = dt.add(weeks=1)
    dt = dt.add(hours=1)

    assert_datetime(dt, 2015, 3, 15, 2, 0, 0)
    assert dt.timezone_name == "-06:00"
    assert dt.offset == -6 * 3600


def test_add_time_to_new_transition_skipped():
    dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 1, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 3, 31, 3, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = pendulum.datetime(2013, 3, 10, 1, 59, 59, 999999, tz="America/New_York")

    assert_datetime(dt, 2013, 3, 10, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 3, 10, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = pendulum.datetime(1957, 4, 28, 1, 59, 59, 999999, tz="America/New_York")

    assert_datetime(dt, 1957, 4, 28, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 1957, 4, 28, 3, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()


def test_add_time_to_new_transition_skipped_big():
    dt = pendulum.datetime(2013, 3, 31, 1, tz="Europe/Paris")

    assert_datetime(dt, 2013, 3, 31, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = dt.add(weeks=1)

    assert_datetime(dt, 2013, 4, 7, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()


def test_add_time_to_new_transition_repeated():
    dt = pendulum.datetime(2013, 10, 27, 1, 59, 59, 999999, tz="Europe/Paris")
    dt = dt.add(hours=1)

    assert_datetime(dt, 2013, 10, 27, 2, 59, 59, 999999)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 10, 27, 2, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()

    dt = pendulum.datetime(2013, 11, 3, 0, 59, 59, 999999, tz="America/New_York")
    dt = dt.add(hours=1)

    assert_datetime(dt, 2013, 11, 3, 1, 59, 59, 999999)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -4 * 3600
    assert dt.is_dst()

    dt = dt.add(microseconds=1)

    assert_datetime(dt, 2013, 11, 3, 1, 0, 0, 0)
    assert dt.timezone_name == "America/New_York"
    assert dt.offset == -5 * 3600
    assert not dt.is_dst()


def test_add_time_to_new_transition_repeated_big():
    dt = pendulum.datetime(2013, 10, 27, 1, tz="Europe/Paris")

    assert_datetime(dt, 2013, 10, 27, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 7200
    assert dt.is_dst()

    dt = dt.add(weeks=1)

    assert_datetime(dt, 2013, 11, 3, 1, 0, 0, 0)
    assert dt.timezone_name == "Europe/Paris"
    assert dt.offset == 3600
    assert not dt.is_dst()


def test_add_duration_across_transition():
    dt = pendulum.datetime(2017, 3, 11, 10, 45, tz="America/Los_Angeles")
    new = dt + pendulum.duration(hours=24)

    assert_datetime(new, 2017, 3, 12, 11, 45)


def test_add_duration_across_transition_days():
    dt = pendulum.datetime(2017, 3, 11, 10, 45, tz="America/Los_Angeles")
    new = dt + pendulum.duration(days=1)

    assert_datetime(new, 2017, 3, 12, 10, 45)

    dt = pendulum.datetime(2023, 11, 5, 0, 0, tz="America/Chicago")
    new = dt + pendulum.duration(days=1)

    assert_datetime(new, 2023, 11, 6, 0, 0)


def test_interval_over_midnight_tz():
    start = pendulum.datetime(2018, 2, 25, tz="Europe/Paris")
    end = start.add(hours=1)
    interval = end - start
    new_end = start + interval

    assert new_end == end


@pytest.mark.parametrize("method, sign", [("add", 1), ("subtract", -1)])
@pytest.mark.parametrize(
    "tz, start, calendar_units, fixed_units, expected",
    [
        pytest.param(
            "Europe/Sofia",
            (2024, 4, 1, 4),
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T02:59:59+02:00",
            id="spring-forward-gap",
        ),
        pytest.param(
            "Europe/Paris",
            (2013, 3, 24, 2, 30),
            {"weeks": 1},
            {"hours": 1},
            "2013-03-31T04:30:00+02:00",
            id="calendar-gap-normalization",
        ),
        pytest.param(
            "America/New_York",
            (2024, 2, 10, 1, 30),
            {"months": 1},
            {"hours": 25},
            "2024-03-11T03:30:00-04:00",
            id="fixed-hours-over-one-day",
        ),
        pytest.param(
            "Europe/Paris",
            (2012, 10, 27, 1, 59, 59, 999999),
            {"years": 1},
            {"hours": 1, "microseconds": 1},
            "2013-10-27T02:00:00+01:00",
            id="fall-back-forward-shift",
        ),
        pytest.param(
            "Europe/Paris",
            (2013, 11, 27, 2),
            {"months": -1},
            {"microseconds": -1},
            "2013-10-27T02:59:59.999999+02:00",
            id="fall-back-backward-shift",
        ),
        pytest.param(
            "Europe/Sofia",
            (2024, 10, 26, 4, 30),
            {"days": 1},
            {"hours": -1},
            "2024-10-27T03:30:00+02:00",
            id="fall-back-calendar-then-elapsed",
        ),
        pytest.param(
            "Europe/Sofia",
            (2024, 10, 20, 3, 30),
            {"weeks": 1},
            {"minutes": -60},
            "2024-10-27T03:30:00+03:00",
            id="ambiguous-time-fold",
        ),
        pytest.param(
            "Europe/Sofia",
            (2024, 3, 30, 4),
            {"days": 1},
            {"seconds": -0.5},
            "2024-03-31T02:59:59.500000+02:00",
            id="opposite-directions-fractional-seconds",
        ),
        pytest.param(
            "America/New_York",
            (2025, 11, 3, 0, 30),
            {"years": -1},
            {"hours": 2},
            "2024-11-03T01:30:00-05:00",
            id="negative-calendar-positive-elapsed",
        ),
        pytest.param(
            "Australia/Lord_Howe",
            (2024, 10, 7, 2, 30),
            {"days": -1},
            {"microseconds": -1},
            "2024-10-06T01:59:59.999999+10:30",
            id="half-hour-spring-forward",
        ),
        pytest.param(
            "Australia/Lord_Howe",
            (2024, 4, 14, 1),
            {"weeks": -1},
            {"hours": 1},
            "2024-04-07T01:30:00+10:30",
            id="half-hour-fall-back",
        ),
        pytest.param(
            "Europe/Paris",
            (2024, 2, 29, 1, 30),
            {"years": 1, "months": 1, "days": 1},
            {"hours": 2},
            "2025-03-30T04:30:00+02:00",
            id="multiple-calendar-units",
        ),
        pytest.param(
            "Europe/Sofia",
            (2024, 4, 1, 16),
            {"days": -1.5},
            {"seconds": -1},
            "2024-03-31T02:59:59+02:00",
            id="fractional-calendar-days",
        ),
        pytest.param(
            "UTC",
            (2024, 4, 1, 4),
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T03:59:59+00:00",
            id="utc-control",
        ),
        pytest.param(
            None,
            (2024, 4, 1, 4),
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T03:59:59",
            id="naive-control",
        ),
        pytest.param(
            5.5,
            (2024, 1, 31, 4),
            {"months": 1},
            {"seconds": -0.25, "microseconds": -1000001},
            "2024-02-29T03:59:58.749999+05:30",
            id="fixed-offset-month-clamping",
        ),
    ],
)
def test_mixed_arithmetic_applies_calendar_before_elapsed_time(
    method: str,
    sign: int,
    tz: str | float | None,
    start: tuple[int, ...],
    calendar_units: dict[str, int | float],
    fixed_units: dict[str, int | float],
    expected: str,
) -> None:
    dt = pendulum.DateTime.create(*start, tz=tz)
    calendar_args = {unit: sign * value for unit, value in calendar_units.items()}
    fixed_args = {unit: sign * value for unit, value in fixed_units.items()}

    result = getattr(dt, method)(**calendar_args, **fixed_args)

    assert result.isoformat() == expected
    assert result.tzinfo is dt.tzinfo


@pytest.mark.parametrize(
    "tz, expected",
    [
        ("Europe/Sofia", "2024-03-31T02:59:59.500000+02:00"),
        (None, "2024-03-31T03:59:59.500000"),
    ],
)
def test_mixed_arithmetic_preserves_subclass(tz: str | None, expected: str) -> None:
    class Subclass(pendulum.DateTime):
        pass

    dt = Subclass.create(2024, 4, 1, 4, tz=tz)
    result = dt.subtract(days=1, seconds=0.5)

    assert type(result) is Subclass
    assert result.tzinfo is dt.tzinfo
    assert result.isoformat() == expected


def test_naive_mixed_arithmetic_rounds_fractional_units_once() -> None:
    dt = pendulum.naive(2024, 4, 1, 4)
    days = 0.6 / 86_400_000_000
    seconds = 0.0000006

    result = dt.add(days=days, seconds=seconds)  # type: ignore[arg-type]

    assert result.isoformat() == "2024-04-01T04:00:00.000001"
    assert result.tzinfo is None
