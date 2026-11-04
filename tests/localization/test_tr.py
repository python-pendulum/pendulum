from __future__ import annotations

import pendulum


locale = "tr"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 saniye önce"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "2 saniye önce"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 dakika önce"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 dakika önce"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 saat önce"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 saat önce"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 gün önce"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 gün önce"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 hafta önce"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 hafta önce"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 ay önce"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 ay önce"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 yıl önce"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 yıl önce"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 saniye sonra"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 saniye sonra"
    assert d2.diff_for_humans(d, locale=locale) == "1 saniye önce"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 saniye"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 saniye"


def test_format():
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "Pazar"
    assert d.format("ddd", locale=locale) == "Paz"
    assert d.format("MMMM", locale=locale) == "Ağustos"
    assert d.format("MMM", locale=locale) == "Ağu"
    assert d.format("Do", locale=locale) == "28."
    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "28.08.2016"
    assert d.format("LL", locale=locale) == "28 Ağustos 2016"
    assert d.format("LLL", locale=locale) == "28 Ağustos 2016 07:03"
    assert d.format("LLLL", locale=locale) == "Pazar, 28 Ağustos 2016 07:03"
