from __future__ import annotations

import pendulum

from pendulum.locales.locale import Locale


locale = "uk"


def test_diff_for_humans():
    start = pendulum.datetime(2016, 8, 29)

    d = start.subtract(seconds=1)
    assert d.diff_for_humans(start, locale=locale) == "кілька секунд до"

    d = start.subtract(minutes=1)
    assert d.diff_for_humans(start, locale=locale) == "1 хвилина до"

    d = start.subtract(hours=1)
    assert d.diff_for_humans(start, locale=locale) == "1 година до"

    d = start.add(seconds=1)
    assert d.diff_for_humans(start, locale=locale) == "кілька секунд посіля"


def test_ua_is_an_alias_for_uk():
    """
    "ua" is an ISO 3166 country code, not a language code, but it was
    historically used for the Ukrainian locale. It must keep working and
    resolve to the same translations as the correctly named "uk" locale.
    """
    assert Locale.load("ua").translation("units.year") == Locale.load(
        "uk"
    ).translation("units.year")

    start = pendulum.datetime(2016, 8, 29)
    d = start.subtract(seconds=1)
    assert d.diff_for_humans(start, locale="ua") == d.diff_for_humans(
        start, locale="uk"
    )
