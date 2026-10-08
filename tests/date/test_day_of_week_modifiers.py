from __future__ import annotations

import calendar

from datetime import date

import pytest

import pendulum

from pendulum.exceptions import PendulumException
from tests.conftest import assert_date


@pytest.mark.parametrize("first_weekday", range(7))
@pytest.mark.parametrize("date_type", [pendulum.Date, pendulum.DateTime])
def test_weekday_modifiers_ignore_calendar_firstweekday(first_weekday, date_type):
    original_first_weekday = calendar.firstweekday()
    calendar.setfirstweekday(first_weekday)
    try:
        for year, month in [(2024, 2), (2025, 2), (2026, 10)]:
            instance = date_type(year, month, 15)
            if isinstance(instance, pendulum.DateTime):
                instance = instance.set(
                    hour=12,
                    minute=34,
                    second=56,
                    microsecond=789012,
                    tz="Europe/Paris",
                )
            for unit, first_month, last_month in [
                ("month", month, month),
                ("quarter", (month - 1) // 3 * 3 + 1, (month - 1) // 3 * 3 + 3),
                ("year", 1, 12),
            ]:
                for weekday in pendulum.WeekDay:
                    matches = [
                        date(year, m, day)
                        for m in range(first_month, last_month + 1)
                        for day in range(1, calendar.monthrange(year, m)[1] + 1)
                        if date(year, m, day).weekday() == weekday
                    ]
                    for result, expected in [
                        (instance.first_of(unit, weekday), matches[0]),
                        (instance.last_of(unit, weekday), matches[-1]),
                        (instance.nth_of(unit, 1, weekday), matches[0]),
                        (instance.nth_of(unit, 2, weekday), matches[1]),
                    ]:
                        assert_date(result, expected.year, expected.month, expected.day)
                        assert isinstance(result, date_type)
                        if isinstance(result, pendulum.DateTime):
                            assert result.tzinfo is instance.tzinfo
                            assert (
                                result.hour
                                == result.minute
                                == result.second
                                == result.microsecond
                                == 0
                            )
                        assert calendar.firstweekday() == first_weekday
                assert_date(instance.first_of(unit), year, first_month, 1)
                assert_date(
                    instance.last_of(unit),
                    year,
                    last_month,
                    calendar.monthrange(year, last_month)[1],
                )
            for method in [instance.first_of, instance.last_of]:
                with pytest.raises(IndexError):
                    method("month", 7)
                assert calendar.firstweekday() == first_weekday
    finally:
        calendar.setfirstweekday(original_first_weekday)


def test_start_of_week():
    d = pendulum.date(1980, 8, 7).start_of("week")
    assert_date(d, 1980, 8, 4)


def test_start_of_week_from_week_start():
    d = pendulum.date(1980, 8, 4).start_of("week")
    assert_date(d, 1980, 8, 4)


def test_start_of_week_crossing_year_boundary():
    d = pendulum.date(2014, 1, 1).start_of("week")
    assert_date(d, 2013, 12, 30)


def test_end_of_week():
    d = pendulum.date(1980, 8, 7).end_of("week")
    assert_date(d, 1980, 8, 10)


def test_end_of_week_from_week_end():
    d = pendulum.date(1980, 8, 10).end_of("week")
    assert_date(d, 1980, 8, 10)


def test_end_of_week_crossing_year_boundary():
    d = pendulum.date(2013, 12, 31).end_of("week")
    assert_date(d, 2014, 1, 5)


def test_next():
    d = pendulum.date(1975, 5, 21).next()
    assert_date(d, 1975, 5, 28)


def test_next_monday():
    d = pendulum.date(1975, 5, 21).next(pendulum.MONDAY)
    assert_date(d, 1975, 5, 26)


def test_next_saturday():
    d = pendulum.date(1975, 5, 21).next(5)
    assert_date(d, 1975, 5, 24)


def test_next_invalid():
    dt = pendulum.date(1975, 5, 21)

    with pytest.raises(ValueError):
        dt.next(7)


def test_previous():
    d = pendulum.date(1975, 5, 21).previous()
    assert_date(d, 1975, 5, 14)


def test_previous_monday():
    d = pendulum.date(1975, 5, 21).previous(pendulum.MONDAY)
    assert_date(d, 1975, 5, 19)


def test_previous_saturday():
    d = pendulum.date(1975, 5, 21).previous(5)
    assert_date(d, 1975, 5, 17)


def test_previous_invalid():
    dt = pendulum.date(1975, 5, 21)

    with pytest.raises(ValueError):
        dt.previous(7)


def test_first_day_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month")
    assert_date(d, 1975, 11, 1)


def test_first_wednesday_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month", pendulum.WEDNESDAY)
    assert_date(d, 1975, 11, 5)


def test_first_friday_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month", 4)
    assert_date(d, 1975, 11, 7)


def test_last_day_of_month():
    d = pendulum.date(1975, 12, 5).last_of("month")
    assert_date(d, 1975, 12, 31)


def test_last_tuesday_of_month():
    d = pendulum.date(1975, 12, 1).last_of("month", pendulum.TUESDAY)
    assert_date(d, 1975, 12, 30)


def test_last_friday_of_month():
    d = pendulum.date(1975, 12, 5).last_of("month", 4)
    assert_date(d, 1975, 12, 26)


def test_nth_of_month_outside_scope():
    d = pendulum.date(1975, 6, 5)

    with pytest.raises(PendulumException):
        d.nth_of("month", 6, pendulum.MONDAY)


def test_nth_of_month_outside_year():
    d = pendulum.date(1975, 12, 5)

    with pytest.raises(PendulumException):
        d.nth_of("month", 55, pendulum.MONDAY)


def test_nth_of_month_first():
    d = pendulum.date(1975, 12, 5).nth_of("month", 1, pendulum.MONDAY)

    assert_date(d, 1975, 12, 1)


def test_2nd_monday_of_month():
    d = pendulum.date(1975, 12, 5).nth_of("month", 2, pendulum.MONDAY)

    assert_date(d, 1975, 12, 8)


def test_3rd_wednesday_of_month():
    d = pendulum.date(1975, 12, 5).nth_of("month", 3, 2)

    assert_date(d, 1975, 12, 17)


def test_first_day_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter")
    assert_date(d, 1975, 10, 1)


def test_first_wednesday_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter", pendulum.WEDNESDAY)
    assert_date(d, 1975, 10, 1)


def test_first_friday_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter", 4)
    assert_date(d, 1975, 10, 3)


def test_first_of_quarter_from_a_day_that_will_not_exist_in_the_first_month():
    d = pendulum.date(2014, 5, 31).first_of("quarter")
    assert_date(d, 2014, 4, 1)


def test_last_day_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter")
    assert_date(d, 1975, 9, 30)


def test_last_tuesday_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter", pendulum.TUESDAY)
    assert_date(d, 1975, 9, 30)


def test_last_friday_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter", pendulum.FRIDAY)
    assert_date(d, 1975, 9, 26)


def test_last_day_of_quarter_that_will_not_exist_in_the_last_month():
    d = pendulum.date(2014, 5, 31).last_of("quarter")
    assert_date(d, 2014, 6, 30)


def test_nth_of_quarter_outside_scope():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("quarter", 20, pendulum.MONDAY)


def test_nth_of_quarter_outside_year():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("quarter", 55, pendulum.MONDAY)


def test_nth_of_quarter_first():
    d = pendulum.date(1975, 12, 5).nth_of("quarter", 1, pendulum.MONDAY)

    assert_date(d, 1975, 10, 6)


def test_nth_of_quarter_from_a_day_that_will_not_exist_in_the_first_month():
    d = pendulum.date(2014, 5, 31).nth_of("quarter", 2, pendulum.MONDAY)
    assert_date(d, 2014, 4, 14)


def test_2nd_monday_of_quarter():
    d = pendulum.date(1975, 8, 5).nth_of("quarter", 2, pendulum.MONDAY)
    assert_date(d, 1975, 7, 14)


def test_3rd_wednesday_of_quarter():
    d = pendulum.date(1975, 8, 5).nth_of("quarter", 3, 2)
    assert_date(d, 1975, 7, 16)


def test_first_day_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year")
    assert_date(d, 1975, 1, 1)


def test_first_wednesday_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year", pendulum.WEDNESDAY)
    assert_date(d, 1975, 1, 1)


def test_first_friday_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year", 4)
    assert_date(d, 1975, 1, 3)


def test_last_day_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year")
    assert_date(d, 1975, 12, 31)


def test_last_tuesday_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year", pendulum.TUESDAY)
    assert_date(d, 1975, 12, 30)


def test_last_friday_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year", 4)
    assert_date(d, 1975, 12, 26)


def test_nth_of_year_outside_scope():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("year", 55, pendulum.MONDAY)


def test_nth_of_year_first():
    d = pendulum.date(1975, 12, 5).nth_of("year", 1, pendulum.MONDAY)

    assert_date(d, 1975, 1, 6)


def test_2nd_monday_of_year():
    d = pendulum.date(1975, 8, 5).nth_of("year", 2, pendulum.MONDAY)
    assert_date(d, 1975, 1, 13)


def test_2rd_wednesday_of_year():
    d = pendulum.date(1975, 8, 5).nth_of("year", 3, pendulum.WEDNESDAY)
    assert_date(d, 1975, 1, 15)


def test_7th_thursday_of_year():
    d = pendulum.date(1975, 8, 31).nth_of("year", 7, pendulum.THURSDAY)
    assert_date(d, 1975, 2, 13)


def test_first_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.first_of("invalid", 3)


def test_last_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.last_of("invalid", 3)


def test_nth_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.nth_of("invalid", 3, pendulum.MONDAY)
