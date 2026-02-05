from __future__ import annotations

import pytest

import pendulum

from tests.conftest import assert_datetime


def test_from_format_returns_datetime():
    d = pendulum.from_format("1975-05-21 22:32:11", "YYYY-MM-DD HH:mm:ss")
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert isinstance(d, pendulum.DateTime)
    assert d.timezone_name == "UTC"


def test_from_format_rejects_extra_text():
    with pytest.raises(ValueError):
        pendulum.from_format("1975-05-21 22:32:11 extra text", "YYYY-MM-DD HH:mm:ss")


def test_from_format_with_timezone_string():
    d = pendulum.from_format(
        "1975-05-21 22:32:11", "YYYY-MM-DD HH:mm:ss", tz="Europe/London"
    )
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert d.timezone_name == "Europe/London"


def test_from_format_with_timezone():
    d = pendulum.from_format(
        "1975-05-21 22:32:11",
        "YYYY-MM-DD HH:mm:ss",
        tz=pendulum.timezone("Europe/London"),
    )
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert d.timezone_name == "Europe/London"


def test_from_format_with_square_bracket_in_timezone():
    with pytest.raises(ValueError, match=r"^String does not match format"):
        pendulum.from_format(
            "1975-05-21 22:32:11 Eu[rope/London",
            "YYYY-MM-DD HH:mm:ss z",
        )


def test_from_format_with_escaped_elements():
    d = pendulum.from_format("1975-05-21T22:32:11+00:00", "YYYY-MM-DD[T]HH:mm:ssZ")
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert d.timezone_name == "+00:00"


def test_from_format_with_escaped_elements_valid_tokens():
    d = pendulum.from_format("1975-05-21T22:32:11.123Z", "YYYY-MM-DD[T]HH:mm:ss.SSS[Z]")
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert d.timezone_name == "UTC"


def test_from_format_with_millis():
    d = pendulum.from_format("1975-05-21 22:32:11.123456", "YYYY-MM-DD HH:mm:ss.SSSSSS")
    assert_datetime(d, 1975, 5, 21, 22, 32, 11, 123456)


def test_from_format_with_padded_day():
    d = pendulum.from_format("Apr  2 12:00:00 2020 GMT", "MMM DD HH:mm:ss YYYY z")
    assert_datetime(d, 2020, 4, 2, 12)


def test_from_format_with_invalid_padded_day():
    with pytest.raises(ValueError):
        pendulum.from_format("Apr   2 12:00:00 2020 GMT", "MMM DD HH:mm:ss YYYY z")


@pytest.mark.parametrize(
    "text,fmt,expected,now",
    [
        ("2014-4", "YYYY-Q", "2014-10-01T00:00:00+00:00", None),
        ("12-02-1999", "MM-DD-YYYY", "1999-12-02T00:00:00+00:00", None),
        ("12-02-1999", "DD-MM-YYYY", "1999-02-12T00:00:00+00:00", None),
        ("12/02/1999", "DD/MM/YYYY", "1999-02-12T00:00:00+00:00", None),
        ("12_02_1999", "DD_MM_YYYY", "1999-02-12T00:00:00+00:00", None),
        ("12:02:1999", "DD:MM:YYYY", "1999-02-12T00:00:00+00:00", None),
        ("2-2-99", "D-M-YY", "1999-02-02T00:00:00+00:00", None),
        ("99", "YY", "1999-01-01T00:00:00+00:00", None),
        ("300-1999", "DDD-YYYY", "1999-10-27T00:00:00+00:00", None),
        ("12-02-1999 2:45:10", "DD-MM-YYYY h:m:s", "1999-02-12T02:45:10+00:00", None),
        ("12-02-1999 12:45:10", "DD-MM-YYYY h:m:s", "1999-02-12T12:45:10+00:00", None),
        ("12:00:00", "HH:mm:ss", "2015-11-12T12:00:00+00:00", None),
        ("12:30:00", "HH:mm:ss", "2015-11-12T12:30:00+00:00", None),
        ("00:00:00", "HH:mm:ss", "2015-11-12T00:00:00+00:00", None),
        ("00:30:00 1", "HH:mm:ss S", "2015-11-12T00:30:00.100000+00:00", None),
        ("00:30:00 12", "HH:mm:ss SS", "2015-11-12T00:30:00.120000+00:00", None),
        ("00:30:00 123", "HH:mm:ss SSS", "2015-11-12T00:30:00.123000+00:00", None),
        ("1234567890", "X", "2009-02-13T23:31:30+00:00", None),
        ("1234567890123", "x", "2009-02-13T23:31:30.123000+00:00", None),
        ("2016-10-06", "YYYY-MM-DD", "2016-10-06T00:00:00+00:00", None),
        ("Tuesday", "dddd", "2015-11-10T00:00:00+00:00", None),
        ("Monday", "dddd", "2018-01-29T00:00:00+00:00", "2018-02-02"),
        ("Mon", "ddd", "2018-01-29T00:00:00+00:00", "2018-02-02"),
        ("Mo", "dd", "2018-01-29T00:00:00+00:00", "2018-02-02"),
        ("0", "d", "2018-01-29T00:00:00+00:00", "2018-02-02"),
        ("6", "d", "2018-02-04T00:00:00+00:00", "2018-02-02"),
        ("1", "E", "2018-01-29T00:00:00+00:00", "2018-02-02"),
        ("March", "MMMM", "2018-03-01T00:00:00+00:00", "2018-02-02"),
        ("Mar", "MMM", "2018-03-01T00:00:00+00:00", "2018-02-02"),
        (
            "Thursday 25th December 1975 02:15:16 PM",
            "dddd Do MMMM YYYY hh:mm:ss A",
            "1975-12-25T14:15:16+00:00",
            None,
        ),
        (
            "Thursday 25th December 1975 02:15:16 PM -05:00",
            "dddd Do MMMM YYYY hh:mm:ss A Z",
            "1975-12-25T14:15:16-05:00",
            None,
        ),
        (
            "1975-12-25T14:15:16 America/Guayaquil",
            "YYYY-MM-DDTHH:mm:ss z",
            "1975-12-25T14:15:16-05:00",
            None,
        ),
        (
            "1975-12-25T14:15:16 America/New_York",
            "YYYY-MM-DDTHH:mm:ss z",
            "1975-12-25T14:15:16-05:00",
            None,
        ),
        (
            "1975-12-25T14:15:16 Africa/Porto-Novo",
            "YYYY-MM-DDTHH:mm:ss z",
            "1975-12-25T14:15:16+01:00",
            None,
        ),
        (
            "1975-12-25T14:15:16 Etc/GMT+0",
            "YYYY-MM-DDTHH:mm:ss z",
            "1975-12-25T14:15:16+00:00",
            None,
        ),
        (
            "1975-12-25T14:15:16 W-SU",
            "YYYY-MM-DDTHH:mm:ss z",
            "1975-12-25T14:15:16+03:00",
            None,
        ),
        ("190022215", "YYDDDDHHmm", "2019-01-02T22:15:00+00:00", None),
    ],
)
def test_from_format(text, fmt, expected, now):
    now = pendulum.datetime(2015, 11, 12) if now is None else pendulum.parse(now)

    with pendulum.travel_to(now, freeze=True):
        assert pendulum.from_format(text, fmt).isoformat() == expected


@pytest.mark.parametrize(
    "text,fmt,expected",
    [
        ("lundi", "dddd", "2018-01-29T00:00:00+00:00"),
        ("lun.", "ddd", "2018-01-29T00:00:00+00:00"),
        ("lu", "dd", "2018-01-29T00:00:00+00:00"),
        ("mars", "MMMM", "2018-03-01T00:00:00+00:00"),
        ("mars", "MMM", "2018-03-01T00:00:00+00:00"),
    ],
)
def test_from_format_with_locale(text, fmt, expected):
    now = pendulum.datetime(2018, 2, 2)

    with pendulum.travel_to(now, freeze=True):
        formatted = pendulum.from_format(text, fmt, locale="fr").isoformat()
        assert formatted == expected


@pytest.mark.parametrize(
    "text,fmt,locale",
    [
        ("23:00", "hh:mm", "en"),
        ("23:00 am", "HH:mm a", "en"),
        ("invalid", "dddd", "en"),
        ("invalid", "ddd", "en"),
        ("invalid", "dd", "en"),
        ("invalid", "MMMM", "en"),
        ("invalid", "MMM", "en"),
    ],
)
def test_from_format_error(text, fmt, locale):
    now = pendulum.datetime(2018, 2, 2)

    with pendulum.travel_to(now, freeze=True), pytest.raises(ValueError):
        pendulum.from_format(text, fmt, locale=locale)


def test_strptime():
    d = pendulum.DateTime.strptime("1975-05-21 22:32:11", "%Y-%m-%d %H:%M:%S")
    assert_datetime(d, 1975, 5, 21, 22, 32, 11)
    assert isinstance(d, pendulum.DateTime)
    assert d.timezone_name == "UTC"


def test_from_format_2_digit_year():
    """
    Complies with open group spec for 2 digit years
    https://pubs.opengroup.org/onlinepubs/9699919799/

    "If century is not specified, then values in the range [69,99] shall
    refer to years 1969 to 1999 inclusive, and values in the
    range [00,68] shall refer to years 2000 to 2068 inclusive."
    """
    d = pendulum.from_format("00", "YY")
    assert d.year == 2000

    d = pendulum.from_format("68", "YY")
    assert d.year == 2068

    d = pendulum.from_format("69", "YY")
    assert d.year == 1969

    d = pendulum.from_format("99", "YY")
    assert d.year == 1999
