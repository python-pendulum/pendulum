from __future__ import annotations

import pendulum


def test_week():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(start=start_date, end=start_date.add(weeks=1))
    assert interval.in_words() == "1 week"


def test_week_and_day():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(start=start_date, end=start_date.add(weeks=1, days=1))
    assert interval.in_words() == "1 week 1 day"


def test_all():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date,
        end=start_date.add(years=1, months=1, days=1, seconds=1, microseconds=1),
    )
    assert interval.in_words() == "1 year 1 month 1 day 1 second"


def test_in_french():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date,
        end=start_date.add(years=1, months=1, days=1, seconds=1, microseconds=1),
    )
    assert interval.in_words(locale="fr") == "1 an 1 mois 1 jour 1 seconde"


def test_singular_negative_values():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(start=start_date, end=start_date.subtract(days=1))
    assert interval.in_words() == "-1 day"


def test_separator():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date,
        end=start_date.add(years=1, months=1, days=1, seconds=1, microseconds=1),
    )
    assert interval.in_words(separator=", ") == "1 year, 1 month, 1 day, 1 second"


def test_subseconds():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date, end=start_date.add(microseconds=123456)
    )
    assert interval.in_words() == "0.12 second"


def test_negative_subseconds():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date.add(microseconds=123456), end=start_date
    )
    assert interval.in_words() == "-0.12 second"


def test_subseconds_with_seconds():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(
        start=start_date, end=start_date.add(seconds=12, microseconds=123456)
    )
    assert interval.in_words() == "12 seconds"


def test_zero_interval():
    start_date = pendulum.datetime(2012, 1, 1)
    interval = pendulum.interval(start=start_date, end=start_date)
    assert interval.in_words() == "0 microseconds"
