from __future__ import annotations

import pendulum


locale = "ko"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1초 전"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "2초 전"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1분 전"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2분 전"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1시간 전"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2시간 전"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1일 전"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2일 전"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1주 전"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2주 전"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1개월 전"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2개월 전"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1년 전"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2년 전"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1초 후"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1초 후"
    assert d2.diff_for_humans(d, locale=locale) == "1초 전"

    assert d.diff_for_humans(d2, True, locale=locale) == "1초"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2초"
