from __future__ import annotations

import pytest

import pendulum

from pendulum.formatting import Formatter


@pytest.mark.parametrize(
    "year, full, short",
    [
        (1, "0001", "01"),
        (9, "0009", "09"),
        (10, "0010", "10"),
        (99, "0099", "99"),
        (100, "0100", "00"),
        (101, "0101", "01"),
        (999, "0999", "99"),
        (1000, "1000", "00"),
        (2009, "2009", "09"),
        (9999, "9999", "99"),
    ],
)
def test_year_tokens_have_fixed_width(year: int, full: str, short: str) -> None:
    value = pendulum.datetime(year, 3, 14)
    assert Formatter().format(value, "YYYY YY Y") == f"{full} {short} {year}"
    assert value.format("YYYY-MM-DD") == f"{full}-03-14"
    assert value.format("YY-MM-DD") == f"{short}-03-14"
    assert pendulum.from_format(value.format("YYYY-MM-DD"), "YYYY-MM-DD") == value


def test_year_padding_applies_to_localized_long_formats() -> None:
    value = pendulum.datetime(42, 3, 14)
    assert value.format("L", locale="en") == "03/14/0042"
    assert value.format("[YYYY] YYYY [YY] YY [Y] Y") == "YYYY 0042 YY 42 Y 42"
