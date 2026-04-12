from __future__ import annotations

import pendulum


locale = "uk"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2026, 4, 3), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "кілька секунд тому"

    # Backward compatibility.
    assert d.diff_for_humans(locale=locale) == d.diff_for_humans(locale="ua")

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "кілька секунд тому"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "21 секунду тому"

    d = pendulum.now().subtract(seconds=22)
    assert d.diff_for_humans(locale=locale) == "22 секунди тому"

    d = pendulum.now().subtract(seconds=25)
    assert d.diff_for_humans(locale=locale) == "25 секунд тому"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 хвилину тому"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 хвилини тому"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "5 хвилин тому"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 годину тому"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 години тому"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "5 годин тому"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 день тому"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 дні тому"

    d = pendulum.now().subtract(days=5)
    assert d.diff_for_humans(locale=locale) == "5 днів тому"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 тиждень тому"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 тижні тому"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 місяць тому"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 місяці тому"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "5 місяців тому"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 рік тому"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 роки тому"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "5 років тому"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "через кілька секунд"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "через кілька секунд"
    assert d2.diff_for_humans(d, locale=locale) == "кілька секунд тому"

    assert d.diff_for_humans(d2, True, locale=locale) == "кілька секунд"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "кілька секунд"

    d = pendulum.now().add(seconds=20)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "через 20 секунд"
    assert d2.diff_for_humans(d, locale=locale) == "20 секунд тому"

    d = pendulum.now().add(seconds=10)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, True, locale=locale) == "кілька секунд"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "11 секунд"


def test_format():
    d = pendulum.datetime(2026, 4, 3, 1, 2, 5, 123456)
    assert (
        d.format("dddd", locale=locale) == "пʼятницю"
    )  # Suboptimal, should be п'ятниця, but clock defines it like that.
    assert d.format("ddd", locale=locale) == "пт"
    assert d.format("MMMM", locale=locale) == "квітня"
    assert d.format("MMM", locale=locale) == "квіт."
    assert d.format("A", locale=locale) == ""
    assert d.format("Qo", locale=locale) == "2"
    assert d.format("Mo", locale=locale) == "4"
    assert d.format("Do", locale=locale) == "3"

    assert d.format("LT", locale=locale) == "01:02"
    assert d.format("LTS", locale=locale) == "01:02:05"
    assert d.format("L", locale=locale) == "03.04.2026"
    assert d.format("LL", locale=locale) == "3 квітня 2026"
    assert d.format("LLL", locale=locale) == "3 квітня 2026, 01:02"
    assert (
        d.format("LLLL", locale=locale) == "пт, 3 квітня 2026, 01:02"
    )  # See note about dddd above.
