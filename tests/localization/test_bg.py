from __future__ import annotations

import pendulum


locale = "bg"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 секунда"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 секунди"

    d = pendulum.now().subtract(seconds=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 секунди"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "преди 21 секунди"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 минута"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 минути"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 минути"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 час"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 часа"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 часа"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 ден"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 дни"

    d = pendulum.now().subtract(days=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 дни"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 седмица"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 седмици"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 месец"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 месеца"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 месеца"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "преди 1 година"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "преди 2 години"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "преди 5 години"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "след 1 секунда"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "след 1 секунда"
    assert d2.diff_for_humans(d, locale=locale) == "преди 1 секунда"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 секунда"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 секунди"