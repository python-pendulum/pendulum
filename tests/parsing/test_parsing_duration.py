from __future__ import annotations

import pytest

from pendulum.parsing import ParserError
from pendulum.parsing import parse


def test_parse_duration():
    text = "P2Y3M4DT5H6M7S"
    parsed = parse(text)

    assert parsed.years == 2
    assert parsed.months == 3
    assert parsed.weeks == 0
    assert parsed.remaining_days == 4
    assert parsed.hours == 5
    assert parsed.minutes == 6
    assert parsed.remaining_seconds == 7
    assert parsed.microseconds == 0

    text = "P1Y2M3DT4H5M6.5S"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 4
    assert parsed.minutes == 5
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y2M3DT4H5M6,5S"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 4
    assert parsed.minutes == 5
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y2M3D"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1Y2M3.5D"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1Y2M3,5D"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT4H54M6.5S"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 4
    assert parsed.minutes == 54
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "PT4H54M6,5S"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 4
    assert parsed.minutes == 54
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y"
    parsed = parse(text)

    assert parsed.years == 1
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5Y"
    with pytest.raises(ParserError):
        parse(text)

    text = "P1,5Y"
    with pytest.raises(ParserError):
        parse(text)

    text = "P1M"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 1
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5M"
    with pytest.raises(ParserError):
        parse(text)

    text = "P1,5M"
    with pytest.raises(ParserError):
        parse(text)

    text = "P1W"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5W"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1,5W"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1D"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5D"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1,5D"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1H"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1.5H"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 30
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1,5H"
    parsed = parse(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 30
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0


def test_parse_duration_no_operator():
    with pytest.raises(ParserError):
        parse("2Y3M4DT5H6M7S")


def test_parse_duration_weeks_combined():
    with pytest.raises(ParserError):
        parse("P1Y2W")


def test_parse_duration_invalid_order():
    with pytest.raises(ParserError):
        parse("P1S")

    with pytest.raises(ParserError):
        parse("P1D1S")

    with pytest.raises(ParserError):
        parse("1Y2M3D1SPT1M")

    with pytest.raises(ParserError):
        parse("P1Y2M3D2MT1S")

    with pytest.raises(ParserError):
        parse("P2M3D1ST1Y1M")

    with pytest.raises(ParserError):
        parse("P1Y2M2MT3D1S")

    with pytest.raises(ParserError):
        parse("P1D1Y1M")

    with pytest.raises(ParserError):
        parse("PT1S1H")


@pytest.mark.parametrize(
    "text",
    [
        "P1Y2Y",
        "P12M4M",
        "P1W2W",
        "P1D2D",
        "PT1H2H",
        "PT12M3M1M",
        "PT1S2S",
        "P0Y0Y",
        "P0M0M",
        "P0W0W",
        "P0D0D",
        "PT0H0H",
        "PT0M0M",
        "PT0S0S",
        "P0M1Y",
        "P0D1M",
        "P0D1Y",
        "PT0M1H",
        "PT0S1M",
        "PT0S1H",
    ],
)
def test_parse_duration_repeated_or_reordered_components(text: str) -> None:
    with pytest.raises(ParserError):
        parse(text)


@pytest.mark.parametrize("text", ["P0Y0M0DT0H0M0S", "P0W"])
def test_parse_duration_zero_components(text: str) -> None:
    parsed = parse(text)
    assert (
        parsed.years,
        parsed.months,
        parsed.weeks,
        parsed.remaining_days,
        parsed.hours,
        parsed.minutes,
        parsed.remaining_seconds,
        parsed.microseconds,
    ) == (0, 0, 0, 0, 0, 0, 0, 0)


def test_parse_duration_invalid():
    with pytest.raises(ParserError):
        parse("P1Dasdfasdf")


def test_parse_interval_invalid():
    with pytest.raises(ParserError):
        parse("/no_start")

    with pytest.raises(ParserError):
        parse("no_end/")


def test_parse_duration_fraction_only_allowed_on_last_component():
    with pytest.raises(ParserError):
        parse("P2Y3M4DT5.5H6M7S")
