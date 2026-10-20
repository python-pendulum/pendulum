from __future__ import annotations

import pytest

import pendulum


def test_to_string():
    d = pendulum.datetime(1975, 12, 25, 0, 0, 0, 0, tz="local")
    assert str(d) == "1975-12-25 00:00:00-05:00"
    d = pendulum.datetime(1975, 12, 25, 0, 0, 0, 123456, tz="local")
    assert str(d) == "1975-12-25 00:00:00.123456-05:00"


def test_to_date_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16)

    assert d.to_date_string() == "1975-12-25"


def test_to_formatted_date_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16)

    assert d.to_formatted_date_string() == "Dec 25, 1975"


def test_to_timestring():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16)

    assert d.to_time_string() == "14:15:16"


def test_to_atom_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_atom_string() == "1975-12-25T14:15:16-05:00"


def test_to_cookie_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_cookie_string() == "Thursday, 25-Dec-1975 14:15:16 EST"


def test_to_iso8601_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_iso8601_string() == "1975-12-25T14:15:16-05:00"


def test_to_iso8601_string_utc():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16)
    assert d.to_iso8601_string() == "1975-12-25T14:15:16Z"


def test_to_iso8601_extended_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, 123456, tz="local")
    assert d.to_iso8601_string() == "1975-12-25T14:15:16.123456-05:00"


def test_to_rfc822_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc822_string() == "Thu, 25 Dec 75 14:15:16 -0500"


def test_to_rfc850_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc850_string() == "Thursday, 25-Dec-75 14:15:16 EST"


def test_to_rfc1036_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc1036_string() == "Thu, 25 Dec 75 14:15:16 -0500"


def test_to_rfc1123_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc1123_string() == "Thu, 25 Dec 1975 14:15:16 -0500"


def test_to_rfc2822_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc2822_string() == "Thu, 25 Dec 1975 14:15:16 -0500"


def test_to_rfc3339_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rfc3339_string() == "1975-12-25T14:15:16-05:00"


def test_to_rfc3339_extended_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, 123456, tz="local")
    assert d.to_rfc3339_string() == "1975-12-25T14:15:16.123456-05:00"


def test_to_rss_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_rss_string() == "Thu, 25 Dec 1975 14:15:16 -0500"


def test_to_w3c_string():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.to_w3c_string() == "1975-12-25T14:15:16-05:00"


@pytest.mark.parametrize(
    "method, expected",
    [
        ("to_cookie_string", "Thursday, 25-Dec-1975 14:15:16 EST"),
        ("to_rfc822_string", "Thu, 25 Dec 75 14:15:16 -0500"),
        ("to_rfc850_string", "Thursday, 25-Dec-75 14:15:16 EST"),
        ("to_rfc1036_string", "Thu, 25 Dec 75 14:15:16 -0500"),
        ("to_rfc1123_string", "Thu, 25 Dec 1975 14:15:16 -0500"),
        ("to_rfc2822_string", "Thu, 25 Dec 1975 14:15:16 -0500"),
        ("to_rss_string", "Thu, 25 Dec 1975 14:15:16 -0500"),
    ],
)
def test_common_formats_are_not_localized(method, expected):
    pendulum.set_locale("fr")
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert getattr(d, method)() == expected


def test_to_string_invalid():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")

    with pytest.raises(ValueError):
        d._to_string("invalid")


def test_repr():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    expected = f"DateTime(1975, 12, 25, 14, 15, 16, tzinfo={d.tzinfo!r})"
    assert repr(d) == expected

    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, 123456, tz="local")
    expected = f"DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo={d.tzinfo!r})"
    assert repr(d) == expected


def test_format_with_locale():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    expected = "jeudi 25e jour de décembre 1975 02:15:16 PM -05:00"
    assert d.format("dddd Do [jour de] MMMM YYYY hh:mm:ss A Z", locale="fr") == expected


def test_strftime():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.strftime("%d") == "25"


def test_for_json():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="local")
    assert d.for_json() == "1975-12-25T14:15:16-05:00"


def test_format():
    d = pendulum.datetime(1975, 12, 25, 14, 15, 16, tz="Europe/Paris")
    assert f"{d}" == "1975-12-25 14:15:16+01:00"
    assert f"{d:YYYY}" == "1975"
    assert f"{d:%Y}" == "1975"
    assert f"{d:%H:%M %d.%m.%Y}" == "14:15 25.12.1975"
