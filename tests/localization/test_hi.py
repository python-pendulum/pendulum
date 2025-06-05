from __future__ import annotations

import pendulum


locale = "hi"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2025, 6, 4), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == 'कुछ सेकंड पहले'

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == 'कुछ सेकंड पहले'

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == '21 सेकंड पहले'

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == '1 मिनट पहले'

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == '2 मिनट पहले'

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == '1 घंटे पहले'

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == '2 घंटे पहले'

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == '1 दिन पहले'

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == '2 दिन पहले'

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == '1 सप्ताह पहले'

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == '2 सप्ताह पहले'

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == '1 माह पहले'

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == '2 माह पहले'

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == '1 वर्ष पहले'

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == '2 वर्ष पहले'

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == 'कुछ सेकंड में'

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == 'कुछ सेकंड बाद'
    assert d2.diff_for_humans(d, locale=locale) == 'कुछ सेकंड पहले'

    assert d.diff_for_humans(d2, True, locale=locale) == 'कुछ सेकंड'
    assert d2.diff_for_humans(d.add(seconds=1), True,
                              locale=locale) == 'कुछ सेकंड'
