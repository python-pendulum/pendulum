from __future__ import annotations

import datetime

import pytest

import pendulum

from pendulum.parsing import ParserError
from pendulum.parsing import parse


def test_y():
    text = "2016"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 1
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_ym():
    text = "2016-10"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_ymd():
    text = "2016-10-06"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_ymd_one_character():
    text = "2016-2-6"

    parsed = parse(text, strict=False)

    assert parsed.year == 2016
    assert parsed.month == 2
    assert parsed.day == 6
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_ymd_hms():
    text = "2016-10-06 12:34:56"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2016-10-06 12:34:56.123456"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 123456
    assert parsed.tzinfo is None


def test_rfc_3339():
    text = "2016-10-06T12:34:56+05:30"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 0
    assert parsed.utcoffset().total_seconds() == 19800


def test_rfc_3339_extended():
    text = "2016-10-06T12:34:56.123456+05:30"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 123456
    assert parsed.utcoffset().total_seconds() == 19800

    text = "2016-10-06T12:34:56.000123+05:30"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 123
    assert parsed.utcoffset().total_seconds() == 19800


def test_rfc_3339_extended_nanoseconds():
    text = "2016-10-06T12:34:56.123456789+05:30"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 6
    assert parsed.hour == 12
    assert parsed.minute == 34
    assert parsed.second == 56
    assert parsed.microsecond == 123456
    assert parsed.utcoffset().total_seconds() == 19800


def test_iso_8601_date():
    text = "2012"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012-05-03"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 5
    assert parsed.day == 3
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20120503"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 5
    assert parsed.day == 3
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012-05"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 5
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_iso8601_datetime():
    text = "2016-10-01T14"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 14
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2016-10-01T14:30"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 14
    assert parsed.minute == 30
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20161001T14"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 14
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20161001T1430"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 14
    assert parsed.minute == 30
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20161001T1430+0530"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 10
    assert parsed.day == 1
    assert parsed.hour == 14
    assert parsed.minute == 30
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.utcoffset().total_seconds() == 19800

    text = "2008-09-03T20:56:35.450686+01"

    parsed = parse(text)

    assert parsed.year == 2008
    assert parsed.month == 9
    assert parsed.day == 3
    assert parsed.hour == 20
    assert parsed.minute == 56
    assert parsed.second == 35
    assert parsed.microsecond == 450686
    assert parsed.utcoffset().total_seconds() == 3600


def test_iso8601_week_number():
    text = "2012-W05"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 30
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012W05"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 30
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    # Long Year
    text = "2015W53"

    parsed = parse(text)

    assert parsed.year == 2015
    assert parsed.month == 12
    assert parsed.day == 28
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012-W05-5"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 2
    assert parsed.day == 3
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012W055"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 2
    assert parsed.day == 3
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2009-W53-7"
    parsed = parse(text)

    assert parsed.year == 2010
    assert parsed.month == 1
    assert parsed.day == 3
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2009-W01-1"
    parsed = parse(text)

    assert parsed.year == 2008
    assert parsed.month == 12
    assert parsed.day == 29
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_iso8601_week_number_with_time():
    text = "2012-W05T09"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 30
    assert parsed.hour == 9
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012W05T09"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 30
    assert parsed.hour == 9
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012-W05-5T09"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 2
    assert parsed.day == 3
    assert parsed.hour == 9
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012W055T09"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 2
    assert parsed.day == 3
    assert parsed.hour == 9
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_iso8601_ordinal():
    text = "2012-007"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 7
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "2012007"

    parsed = parse(text)

    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 7
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_iso8601_time():
    now = pendulum.datetime(2015, 11, 12)

    text = "T201205"

    parsed = parse(text, now=now)

    assert parsed.year == 2015
    assert parsed.month == 11
    assert parsed.day == 12
    assert parsed.hour == 20
    assert parsed.minute == 12
    assert parsed.second == 5
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20:12:05"

    parsed = parse(text, now=now)

    assert parsed.year == 2015
    assert parsed.month == 11
    assert parsed.day == 12
    assert parsed.hour == 20
    assert parsed.minute == 12
    assert parsed.second == 5
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "20:12:05.123456"

    parsed = parse(text, now=now)

    assert parsed.year == 2015
    assert parsed.month == 11
    assert parsed.day == 12
    assert parsed.hour == 20
    assert parsed.minute == 12
    assert parsed.second == 5
    assert parsed.microsecond == 123456
    assert parsed.tzinfo is None


def test_iso8601_ordinal_invalid():
    text = "2012-007-05"

    with pytest.raises(ParserError):
        parse(text)


def test_exact():
    text = "2012"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 1

    text = "2012-03"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2012
    assert parsed.month == 3
    assert parsed.day == 1

    text = "2012-03-13"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2012
    assert parsed.month == 3
    assert parsed.day == 13

    text = "2012W055"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2012
    assert parsed.month == 2
    assert parsed.day == 3

    text = "2012007"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.date)
    assert parsed.year == 2012
    assert parsed.month == 1
    assert parsed.day == 7

    text = "20:12:05"

    parsed = parse(text, exact=True)

    assert isinstance(parsed, datetime.time)
    assert parsed.hour == 20
    assert parsed.minute == 12
    assert parsed.second == 5
    assert parsed.microsecond == 0


def test_edge_cases():
    text = "2013-11-1"

    parsed = parse(text, strict=False)
    assert parsed.year == 2013
    assert parsed.month == 11
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "10-01-01"

    parsed = parse(text, strict=False)
    assert parsed.year == 2010
    assert parsed.month == 1
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "31-01-01"

    parsed = parse(text, strict=False)
    assert parsed.year == 2031
    assert parsed.month == 1
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None

    text = "32-01-01"

    parsed = parse(text, strict=False)
    assert parsed.year == 2032
    assert parsed.month == 1
    assert parsed.day == 1
    assert parsed.hour == 0
    assert parsed.minute == 0
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_strict():
    text = "4 Aug 2015 - 11:20 PM"

    with pytest.raises(ParserError):
        parse(text)

    parsed = parse(text, strict=False)
    assert parsed.year == 2015
    assert parsed.month == 8
    assert parsed.day == 4
    assert parsed.hour == 23
    assert parsed.minute == 20
    assert parsed.second == 0
    assert parsed.microsecond == 0
    assert parsed.tzinfo is None


def test_invalid():
    text = "201610T"

    with pytest.raises(ParserError):
        parse(text)

    text = "2012-W54"

    with pytest.raises(ParserError):
        parse(text)

    text = "2012-W13-8"

    with pytest.raises(ParserError):
        parse(text)

    # W53 in normal year (not long)
    text = "2017W53"

    with pytest.raises(ParserError):
        parse(text)

    text = "/2012"

    with pytest.raises(ParserError):
        parse(text)

    text = "2012/"

    with pytest.raises(ParserError):
        parse(text)


def test_exif_edge_case():
    text = "2016:12:26 15:45:28"

    parsed = parse(text)

    assert parsed.year == 2016
    assert parsed.month == 12
    assert parsed.day == 26
    assert parsed.hour == 15
    assert parsed.minute == 45
    assert parsed.second == 28
