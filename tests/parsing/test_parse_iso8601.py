from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import time

import pytest

from pendulum.parsing import parse_iso8601


try:
    from pendulum._pendulum import FixedTimezone
except ImportError:
    from pendulum.tz.timezone import FixedTimezone


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("2016-10", date(2016, 10, 1)),
        ("2016-10-06", date(2016, 10, 6)),
        # Ordinal date
        ("2012-007", date(2012, 1, 7)),
        ("2012007", date(2012, 1, 7)),
        ("2017-079", date(2017, 3, 20)),
        # Week date
        ("2012-W05", date(2012, 1, 30)),
        ("2008-W39-6", date(2008, 9, 27)),
        ("2009-W53-7", date(2010, 1, 3)),
        ("2009-W01-1", date(2008, 12, 29)),
        # Time
        ("12:34", time(12, 34, 0)),
        ("12:34:56", time(12, 34, 56)),
        ("12:34:56.123", time(12, 34, 56, 123000)),
        ("12:34:56.123456", time(12, 34, 56, 123456)),
        ("12:34+05:30", time(12, 34, 0, tzinfo=FixedTimezone(19800))),
        ("12:34:56+05:30", time(12, 34, 56, tzinfo=FixedTimezone(19800))),
        ("12:34:56.123+05:30", time(12, 34, 56, 123000, tzinfo=FixedTimezone(19800))),
        (
            "12:34:56.123456+05:30",
            time(12, 34, 56, 123456, tzinfo=FixedTimezone(19800)),
        ),
        # Datetime
        ("2016-10-06T12:34:56.123456", datetime(2016, 10, 6, 12, 34, 56, 123456)),
        ("2016-10-06T12:34:56.123", datetime(2016, 10, 6, 12, 34, 56, 123000)),
        ("2016-10-06T12:34:56.000123", datetime(2016, 10, 6, 12, 34, 56, 123)),
        ("20161006T12", datetime(2016, 10, 6, 12, 0, 0, 0)),
        ("20161006T123456", datetime(2016, 10, 6, 12, 34, 56, 0)),
        ("20161006T123456.123456", datetime(2016, 10, 6, 12, 34, 56, 123456)),
        ("20161006 123456.123456", datetime(2016, 10, 6, 12, 34, 56, 123456)),
        # Datetime with offset
        (
            "2016-10-06T12:34:56.123456+05:30",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(19800)),
        ),
        (
            "2016-10-06T12:34:56.123456+0530",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(19800)),
        ),
        (
            "2016-10-06T12:34:56.123456-05:30",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-19800)),
        ),
        (
            "2016-10-06T12:34:56.123456-0530",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-19800)),
        ),
        (
            "2016-10-06T12:34:56.123456+05",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(18000)),
        ),
        (
            "2016-10-06T12:34:56.123456-05",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-18000)),
        ),
        (
            "20161006T123456,123456-05",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-18000)),
        ),
        (
            "2016-10-06T12:34:56.123456789+05:30",
            datetime(2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(+19800)),
        ),
        # Week date with time
        ("2008-W39-6T09", datetime(2008, 9, 27, 9, 0, 0, 0)),
    ],
)
def test_parse_iso8601(text: str, expected: date) -> None:
    assert parse_iso8601(text) == expected


def test_parse_iso8601_invalid():
    # Invalid month
    with pytest.raises(ValueError):
        parse_iso8601("20161306T123456")

    # Invalid day
    with pytest.raises(ValueError):
        parse_iso8601("20161033T123456")

    # Invalid day for month
    with pytest.raises(ValueError):
        parse_iso8601("20161131T123456")

    # Invalid hour
    with pytest.raises(ValueError):
        parse_iso8601("20161006T243456")

    # Invalid minute
    with pytest.raises(ValueError):
        parse_iso8601("20161006T126056")

    # Invalid second
    with pytest.raises(ValueError):
        parse_iso8601("20161006T123460")

    # Extraneous separator
    with pytest.raises(ValueError):
        parse_iso8601("20140203 04:05:.123456")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:")

    # Invalid ordinal
    with pytest.raises(ValueError):
        parse_iso8601("2009367")
    with pytest.raises(ValueError):
        parse_iso8601("2009-367")
    with pytest.raises(ValueError):
        parse_iso8601("2015-366")
    with pytest.raises(ValueError):
        parse_iso8601("2015-000")

    # Invalid date
    with pytest.raises(ValueError):
        parse_iso8601("2009-")

    # Invalid time
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19T14:3924")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16.5:23.35:48")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16:23.35:48.45")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16:23.33.600")

    # Invalid offset
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+063")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+06a00")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+0:6:00")

    # Missing time separator
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-1914:39")

    # Invalid week date
    with pytest.raises(ValueError):
        parse_iso8601("2012-W63")
    with pytest.raises(ValueError):
        parse_iso8601("2012-W12-9")
    with pytest.raises(ValueError):
        parse_iso8601("2012W12-3")  # Missing separator
    with pytest.raises(ValueError):
        parse_iso8601("2012-W123")  # Missing separator


@pytest.mark.parametrize(
    ["text", "expected"],
    [
        ("P2Y3M4DT5H6M7S", (2, 3, 0, 4, 5, 6, 7, 0)),
        ("P1Y2M3DT4H5M6.5S", (1, 2, 0, 3, 4, 5, 6, 500_000)),
        ("P1Y2M3DT4H5M6,5S", (1, 2, 0, 3, 4, 5, 6, 500_000)),
        ("P1Y2M3D", (1, 2, 0, 3, 0, 0, 0, 0)),
        ("P1Y2M3.5D", (1, 2, 0, 3, 12, 0, 0, 0)),
        ("P1Y2M3,5D", (1, 2, 0, 3, 12, 0, 0, 0)),
        ("PT4H54M6.5S", (0, 0, 0, 0, 4, 54, 6, 500_000)),
        ("PT4H54M6,5S", (0, 0, 0, 0, 4, 54, 6, 500_000)),
        ("P1Y", (1, 0, 0, 0, 0, 0, 0, 0)),
        ("P1M", (0, 1, 0, 0, 0, 0, 0, 0)),
        ("P1W", (0, 0, 1, 0, 0, 0, 0, 0)),
        ("P1.5W", (0, 0, 1, 3, 12, 0, 0, 0)),
        ("P1,5W", (0, 0, 1, 3, 12, 0, 0, 0)),
        ("P1D", (0, 0, 0, 1, 0, 0, 0, 0)),
        ("P1.5D", (0, 0, 0, 1, 12, 0, 0, 0)),
        ("P1,5D", (0, 0, 0, 1, 12, 0, 0, 0)),
        ("PT1H", (0, 0, 0, 0, 1, 0, 0, 0)),
        ("PT1.5H", (0, 0, 0, 0, 1, 30, 0, 0)),
        ("PT1,5H", (0, 0, 0, 0, 1, 30, 0, 0)),
        ("P2Y30M4DT5H6M7S", (2, 30, 0, 4, 5, 6, 7, 0)),
    ],
)
def test_parse_iso8601_duration(
    text: str, expected: tuple[int, int, int, int, int, int, int, int]
) -> None:
    parsed = parse_iso8601(text)

    assert (
        parsed.years,
        parsed.months,
        parsed.weeks,
        parsed.remaining_days,
        parsed.hours,
        parsed.minutes,
        parsed.remaining_seconds,
        parsed.microseconds,
    ) == expected


def test_parse_iso8601_duration_invalid():
    # Must include at least one element
    with pytest.raises(ValueError):
        parse_iso8601("P")
