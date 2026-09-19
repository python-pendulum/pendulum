from __future__ import annotations

import pendulum


locale = "zh"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1秒钟前"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2分钟前"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2小时前"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2天前"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2周前"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2个月前"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2年前"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1秒钟后"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1秒钟后"
    assert d2.diff_for_humans(d, locale=locale) == "1秒钟前"

    assert d.diff_for_humans(d2, True, locale=locale) == "1秒钟"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2秒钟"
