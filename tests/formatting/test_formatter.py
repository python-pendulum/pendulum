from __future__ import annotations

import pytest

import pendulum

from pendulum.formatting import Formatter
from pendulum.locales.locale import Locale


@pytest.fixture(autouse=True)
def setup():
    Locale._cache["dummy"] = {}

    yield

    del Locale._cache["dummy"]


def test_year_tokens():
    d = pendulum.datetime(2009, 1, 14, 15, 25, 50, 123456)
    f = Formatter()

    assert f.format(d, "YYYY") == "2009"
    assert f.format(d, "YY") == "09"
    assert f.format(d, "Y") == "2009"


def test_quarter_tokens():
    f = Formatter()
    d = pendulum.datetime(1985, 1, 4)
    assert f.format(d, "Q") == "1"

    d = pendulum.datetime(2029, 8, 1)
    assert f.format(d, "Q") == "3"

    d = pendulum.datetime(1985, 1, 4)
    assert f.format(d, "Qo") == "1st"

    d = pendulum.datetime(2029, 8, 1)
    assert f.format(d, "Qo") == "3rd"

    d = pendulum.datetime(1985, 1, 4)
    assert f.format(d, "Qo", locale="fr") == "1er"

    d = pendulum.datetime(2029, 8, 1)
    assert f.format(d, "Qo", locale="fr") == "3e"


def test_month_tokens():
    f = Formatter()
    d = pendulum.datetime(2016, 3, 24)
    assert f.format(d, "MM") == "03"
    assert f.format(d, "M") == "3"

    assert f.format(d, "MMM") == "Mar"
    assert f.format(d, "MMMM") == "March"
    assert f.format(d, "Mo") == "3rd"

    assert f.format(d, "MMM", locale="fr") == "mars"
    assert f.format(d, "MMMM", locale="fr") == "mars"
    assert f.format(d, "Mo", locale="fr") == "3e"


def test_day_tokens():
    f = Formatter()
    d = pendulum.datetime(2016, 3, 7)
    assert f.format(d, "DD") == "07"
    assert f.format(d, "D") == "7"

    assert f.format(d, "Do") == "7th"
    assert f.format(d.first_of("month"), "Do") == "1st"

    assert f.format(d, "Do", locale="fr") == "7e"
    assert f.format(d.first_of("month"), "Do", locale="fr") == "1er"


def test_day_of_year():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)
    assert f.format(d, "DDDD") == "241"
    assert f.format(d, "DDD") == "241"
    assert f.format(d.start_of("year"), "DDDD") == "001"
    assert f.format(d.start_of("year"), "DDD") == "1"

    assert f.format(d, "DDDo") == "241st"
    assert f.format(d.add(days=3), "DDDo") == "244th"

    assert f.format(d, "DDDo", locale="fr") == "241e"
    assert f.format(d.add(days=3), "DDDo", locale="fr") == "244e"


def test_week_of_year():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)

    assert f.format(d, "wo") == "34th"


def test_day_of_week():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)
    assert f.format(d, "d") == "0"

    assert f.format(d, "dd") == "Su"
    assert f.format(d, "ddd") == "Sun"
    assert f.format(d, "dddd") == "Sunday"

    assert f.format(d, "dd", locale="fr") == "di"
    assert f.format(d, "ddd", locale="fr") == "dim."
    assert f.format(d, "dddd", locale="fr") == "dimanche"

    assert f.format(d, "do") == "0th"


def test_localized_day_of_week():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)
    assert f.format(d, "e") == "0"
    assert f.format(d, "e", locale="en-gb") == "6"
    assert f.format(d.add(days=2), "e") == "2"
    assert f.format(d.add(days=2), "e", locale="en-gb") == "1"

    assert f.format(d, "eo") == "1st"
    assert f.format(d, "eo", locale="en-gb") == "7th"
    assert f.format(d.add(days=2), "eo") == "3rd"
    assert f.format(d.add(days=2), "eo", locale="en-gb") == "2nd"


def test_day_of_iso_week():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)
    assert f.format(d, "E") == "7"


def test_am_pm():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 23)
    assert f.format(d, "A") == "PM"
    assert f.format(d.set(hour=11), "A") == "AM"


def test_hour():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7)
    assert f.format(d, "H") == "7"
    assert f.format(d, "HH") == "07"

    d = pendulum.datetime(2016, 8, 28, 0)
    assert f.format(d, "h") == "12"
    assert f.format(d, "hh") == "12"


def test_minute():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3)
    assert f.format(d, "m") == "3"
    assert f.format(d, "mm") == "03"


def test_second():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6)
    assert f.format(d, "s") == "6"
    assert f.format(d, "ss") == "06"


def test_fractional_second():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert f.format(d, "S") == "1"
    assert f.format(d, "SS") == "12"
    assert f.format(d, "SSS") == "123"
    assert f.format(d, "SSSS") == "1234"
    assert f.format(d, "SSSSS") == "12345"
    assert f.format(d, "SSSSSS") == "123456"

    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 0)
    assert f.format(d, "S") == "0"
    assert f.format(d, "SS") == "00"
    assert f.format(d, "SSS") == "000"
    assert f.format(d, "SSSS") == "0000"
    assert f.format(d, "SSSSS") == "00000"
    assert f.format(d, "SSSSSS") == "000000"

    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123)
    assert f.format(d, "S") == "0"
    assert f.format(d, "SS") == "00"
    assert f.format(d, "SSS") == "000"
    assert f.format(d, "SSSS") == "0001"
    assert f.format(d, "SSSSS") == "00012"
    assert f.format(d, "SSSSSS") == "000123"


def test_timezone():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456, tz="Europe/Paris")
    assert f.format(d, "zz") == "CEST"
    assert f.format(d, "z") == "Europe/Paris"

    d = pendulum.datetime(2016, 1, 28, 7, 3, 6, 123456, tz="Europe/Paris")
    assert f.format(d, "zz") == "CET"
    assert f.format(d, "z") == "Europe/Paris"


def test_timezone_offset():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456, tz="Europe/Paris")
    assert f.format(d, "ZZ") == "+0200"
    assert f.format(d, "Z") == "+02:00"

    d = pendulum.datetime(2016, 1, 28, 7, 3, 6, 123456, tz="Europe/Paris")
    assert f.format(d, "ZZ") == "+0100"
    assert f.format(d, "Z") == "+01:00"

    d = pendulum.datetime(2016, 1, 28, 7, 3, 6, 123456, tz="America/Guayaquil")
    assert f.format(d, "ZZ") == "-0500"
    assert f.format(d, "Z") == "-05:00"


def test_timestamp():
    f = Formatter()
    d = pendulum.datetime(1970, 1, 1)
    assert f.format(d, "X") == "0"
    assert f.format(d.add(days=1), "X") == "86400"


def test_timestamp_milliseconds():
    f = Formatter()
    d = pendulum.datetime(1970, 1, 1)
    assert f.format(d, "x") == "0"
    assert f.format(d.add(days=1), "x") == "86400000"
    assert f.format(d.add(days=1, microseconds=129123), "x") == "86400129"


def test_date_formats():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert f.format(d, "LT") == "7:03 AM"
    assert f.format(d, "LTS") == "7:03:06 AM"
    assert f.format(d, "L") == "08/28/2016"
    assert f.format(d, "LL") == "August 28, 2016"
    assert f.format(d, "LLL") == "August 28, 2016 7:03 AM"
    assert f.format(d, "LLLL") == "Sunday, August 28, 2016 7:03 AM"

    assert f.format(d, "LT", locale="fr") == "07:03"
    assert f.format(d, "LTS", locale="fr") == "07:03:06"
    assert f.format(d, "L", locale="fr") == "28/08/2016"
    assert f.format(d, "LL", locale="fr") == "28 août 2016"
    assert f.format(d, "LLL", locale="fr") == "28 août 2016 07:03"
    assert f.format(d, "LLLL", locale="fr") == "dimanche 28 août 2016 07:03"

    assert f.format(d, "LT", locale="ja") == "07:03"
    assert f.format(d, "LTS", locale="ja") == "07:03:06"
    assert f.format(d, "L", locale="ja") == "2016/08/28"
    assert f.format(d, "LL", locale="ja") == "2016年8月28日"
    assert f.format(d, "LLL", locale="ja") == "2016年8月28日 07:03"
    assert f.format(d, "LLLL", locale="ja") == "2016年8月28日 日曜日 07:03"


def test_escape():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28)
    assert f.format(d, r"[YYYY] YYYY \[YYYY\]") == "YYYY 2016 [2016]"
    assert f.format(d, r"\D D \\D") == "D 28 \\28"


def test_date_formats_missing():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)

    assert f.format(d, "LT", locale="dummy") == "7:03 AM"
    assert f.format(d, "LTS", locale="dummy") == "7:03:06 AM"
    assert f.format(d, "L", locale="dummy") == "08/28/2016"
    assert f.format(d, "LL", locale="dummy") == "August 28, 2016"
    assert f.format(d, "LLL", locale="dummy") == "August 28, 2016 7:03 AM"
    assert f.format(d, "LLLL", locale="dummy") == "Sunday, August 28, 2016 7:03 AM"


def test_unknown_token():
    f = Formatter()
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)

    assert f.format(d, "J") == "J"
