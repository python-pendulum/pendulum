from __future__ import annotations

import pendulum


def test_week():
    assert pendulum.duration(days=364).in_words() == "52 weeks"
    assert pendulum.duration(days=7).in_words() == "1 week"


def test_week_to_string():
    assert str(pendulum.duration(days=364)) == "52 weeks"
    assert str(pendulum.duration(days=7)) == "1 week"


def test_weeks_and_day():
    assert pendulum.duration(days=365).in_words() == "52 weeks 1 day"


def test_all():
    pi = pendulum.duration(
        years=2, months=3, days=1177, seconds=7284, microseconds=1000000
    )

    expected = "2 years 3 months 168 weeks 1 day 2 hours 1 minute 25 seconds"
    assert pi.in_words() == expected


def test_in_french():
    pi = pendulum.duration(
        years=2, months=3, days=1177, seconds=7284, microseconds=1000000
    )

    expected = "2 ans 3 mois 168 semaines 1 jour 2 heures 1 minute 25 secondes"
    assert pi.in_words(locale="fr") == expected


def test_repr():
    pi = pendulum.duration(
        years=2, months=3, days=1177, seconds=7284, microseconds=1000000
    )

    expected = (
        "Duration(years=2, months=3, weeks=168, days=1, hours=2, minutes=1, seconds=25)"
    )
    assert repr(pi) == expected


def test_singular_negative_values():
    pi = pendulum.duration(days=-1)

    assert pi.in_words() == "-1 day"


def test_separator():
    pi = pendulum.duration(days=1177, seconds=7284, microseconds=1000000)

    expected = "168 weeks, 1 day, 2 hours, 1 minute, 25 seconds"
    assert pi.in_words(separator=", ") == expected


def test_subseconds():
    pi = pendulum.duration(microseconds=123456)

    assert pi.in_words() == "0.12 seconds"


def test_subseconds_with_seconds():
    pi = pendulum.duration(seconds=12, microseconds=123456)

    assert pi.in_words() == "12 seconds"


def test_duration_with_all_zero_values():
    pi = pendulum.duration()

    assert pi.in_words() == "0 microseconds"
