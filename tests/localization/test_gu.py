from __future__ import annotations

import pendulum


locale = "gu"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2025, 6, 4), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "અમુક સેકંડ પહેલાં"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "અમુક સેકંડ પહેલાં"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "21 સેકંડ પહેલાં"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 મિનિટ પહેલાં"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 મિનિટ પહેલાં"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 કલાક પહેલાં"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 કલાક પહેલાં"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 દિવસ પહેલાં"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 દિવસ પહેલાં"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 અઠવાડિયા પહેલાં"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 અઠવાડિયા પહેલાં"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 મહિના પહેલાં"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 મહિના પહેલાં"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 વર્ષ પહેલાં"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 વર્ષ પહેલાં"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "અમુક સેકંડ માં"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "અમુક સેકંડ પછી"
    assert d2.diff_for_humans(d, locale=locale) == "અમુક સેકંડ પહેલાં"

    assert d.diff_for_humans(d2, True, locale=locale) == "અમુક સેકંડ"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "અમુક સેકંડ"


def test_format():
    d = pendulum.datetime(2016, 8, 29, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "સોમવાર"
    assert d.format("ddd", locale=locale) == "સોમ"
    assert d.format("dd", locale=locale) == "સો"
