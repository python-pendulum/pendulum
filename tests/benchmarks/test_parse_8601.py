from __future__ import annotations

import pytest

from pendulum.parsing.iso8601 import parse_iso8601


@pytest.mark.benchmark(group="Parsing")
def test_parse_iso8601() -> None:
    # Date
    parse_iso8601("2016")
    parse_iso8601("2016-10")
    parse_iso8601("2016-10-06")
    parse_iso8601("20161006")

    # Time
    parse_iso8601("201610")

    # Datetime
    parse_iso8601("2016-10-06T12:34:56.123456")
    parse_iso8601("2016-10-06T12:34:56.123")
    parse_iso8601("2016-10-06T12:34:56.000123")
    parse_iso8601("2016-10-06T12")
    parse_iso8601("2016-10-06T123456")
    parse_iso8601("2016-10-06T123456.123456")
    parse_iso8601("20161006T123456.123456")
    parse_iso8601("20161006 123456.123456")

    # Datetime with offset
    parse_iso8601("2016-10-06T12:34:56.123456+05:30")
    parse_iso8601("2016-10-06T12:34:56.123456+0530")
    parse_iso8601("2016-10-06T12:34:56.123456-05:30")
    parse_iso8601("2016-10-06T12:34:56.123456-0530")
    parse_iso8601("2016-10-06T12:34:56.123456+05")
    parse_iso8601("2016-10-06T12:34:56.123456-05")
    parse_iso8601("20161006T123456,123456-05")
    parse_iso8601("2016-10-06T12:34:56.123456789+05:30")

    # Ordinal date
    parse_iso8601("2012-007")
    parse_iso8601("2012007")
    parse_iso8601("2017-079")

    # Week date
    parse_iso8601("2012-W05")
    parse_iso8601("2008-W39-6")
    parse_iso8601("2009-W53-7")
    parse_iso8601("2009-W01-1")

    # Week date with time
    parse_iso8601("2008-W39-6T09")
