from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from zoneinfo import ZoneInfo

import pytest

import pendulum


@pytest.mark.parametrize("method, sign", [("add", 1), ("subtract", -1)])
@pytest.mark.parametrize(
    "tz, start, calendar_units, fixed_units, calendar_target",
    [
        pytest.param(
            "Europe/Sofia",
            "2024-04-01T04:00:00",
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T04:00:00+03:00",
            id="issue-838",
        ),
        pytest.param(
            "Europe/Paris",
            "2013-03-24T02:30:00",
            {"weeks": 1},
            {"hours": 1},
            "2013-03-31T03:30:00+02:00",
            id="normalize-calendar-gap-first",
        ),
        pytest.param(
            "America/New_York",
            "2024-02-10T01:30:00",
            {"months": 1},
            {"hours": 25},
            "2024-03-10T01:30:00-05:00",
            id="fixed-hours-over-one-day",
        ),
        pytest.param(
            "Europe/Paris",
            "2012-10-27T01:59:59.999999",
            {"years": 1},
            {"hours": 1, "microseconds": 1},
            "2013-10-27T01:59:59.999999+02:00",
            id="forward-fall-back",
        ),
        pytest.param(
            "Europe/Paris",
            "2013-11-27T02:00:00",
            {"months": -1},
            {"microseconds": -1},
            "2013-10-27T02:00:00+01:00",
            id="backward-fall-back",
        ),
        pytest.param(
            "Europe/Sofia",
            "2024-10-20T03:30:00",
            {"weeks": 1},
            {"minutes": -60},
            "2024-10-27T03:30:00+02:00",
            id="calendar-overlap-default-fold",
        ),
        pytest.param(
            "Europe/Sofia",
            "2024-03-30T04:00:00",
            {"days": 1},
            {"seconds": -0.5},
            "2024-03-31T04:00:00+03:00",
            id="opposite-directions-fractional-seconds",
        ),
        pytest.param(
            "America/New_York",
            "2025-11-03T00:30:00",
            {"years": -1},
            {"hours": 2},
            "2024-11-03T00:30:00-04:00",
            id="negative-years-positive-hours",
        ),
        pytest.param(
            "Australia/Lord_Howe",
            "2024-10-07T02:30:00",
            {"days": -1},
            {"microseconds": -1},
            "2024-10-06T02:30:00+11:00",
            id="half-hour-spring-forward",
        ),
        pytest.param(
            "Australia/Lord_Howe",
            "2024-04-14T01:00:00",
            {"weeks": -1},
            {"hours": 1},
            "2024-04-07T01:00:00+11:00",
            id="half-hour-fall-back",
        ),
        pytest.param(
            "Europe/Paris",
            "2024-02-29T01:30:00",
            {"years": 1, "months": 1, "days": 1},
            {"hours": 2},
            "2025-03-30T01:30:00+01:00",
            id="calendar-units-applied-together",
        ),
        pytest.param(
            "Europe/Sofia",
            "2024-04-01T16:00:00",
            {"days": -1.5},
            {"seconds": -1},
            "2024-03-31T04:00:00+03:00",
            id="fractional-calendar-days",
        ),
        pytest.param(
            "UTC",
            "2024-04-01T04:00:00",
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T04:00:00+00:00",
            id="utc-control",
        ),
        pytest.param(
            None,
            "2024-04-01T04:00:00",
            {"days": -1},
            {"seconds": -1},
            "2024-03-31T04:00:00",
            id="naive-control",
        ),
        pytest.param(
            5.5,
            "2024-01-31T04:00:00",
            {"months": 1},
            {"seconds": -0.25, "microseconds": -1000001},
            "2024-02-29T04:00:00+05:30",
            id="fixed-offset-month-clamping",
        ),
    ],
)
def test_mixed_arithmetic_applies_calendar_then_elapsed_time(
    method: str,
    sign: int,
    tz: str | float | None,
    start: str,
    calendar_units: dict[str, int | float],
    fixed_units: dict[str, int | float],
    calendar_target: str,
) -> None:
    native_start = datetime.fromisoformat(start)
    dt = pendulum.DateTime.create(
        native_start.year,
        native_start.month,
        native_start.day,
        native_start.hour,
        native_start.minute,
        native_start.second,
        native_start.microsecond,
        tz=tz,
    )
    operation = getattr(dt, method)
    calendar_args = {unit: sign * value for unit, value in calendar_units.items()}
    fixed_args = {unit: sign * value for unit, value in fixed_units.items()}

    # These explicit targets verify calendar shifting/normalization independently
    # of the mixed call. The elapsed-time oracle uses only stdlib arithmetic.
    calendar_result = operation(**calendar_args)
    assert calendar_result.isoformat() == calendar_target
    expected_calendar = datetime.fromisoformat(calendar_target)
    elapsed = timedelta(**fixed_units)
    if tz is None:
        expected = expected_calendar + elapsed
    else:
        native_tz = (
            ZoneInfo(tz) if isinstance(tz, str) else timezone(timedelta(hours=tz))
        )
        expected = (expected_calendar.astimezone(timezone.utc) + elapsed).astimezone(
            native_tz
        )

    result = operation(**calendar_args, **fixed_args)
    assert result.isoformat() == expected.isoformat()
    assert result.tzinfo is dt.tzinfo
    if expected.replace(fold=0).utcoffset() != expected.replace(fold=1).utcoffset():
        assert result.fold == expected.fold


@pytest.mark.parametrize("tz", ["Europe/Sofia", None])
def test_mixed_arithmetic_preserves_subclass(tz: str | None) -> None:
    class Subclass(pendulum.DateTime):
        pass

    dt = Subclass.create(2024, 4, 1, 4, tz=tz)
    result = dt.subtract(days=1, seconds=0.5)

    assert type(result) is Subclass
    assert result.tzinfo is dt.tzinfo
    assert result.isoformat() == (
        "2024-03-31T02:59:59.500000+02:00"
        if tz is not None
        else "2024-03-31T03:59:59.500000"
    )


def test_naive_mixed_arithmetic_preserves_fractional_rounding() -> None:
    dt = pendulum.naive(2024, 4, 1, 4)
    days = 0.6 / 86_400_000_000
    seconds = 0.0000006

    # Round the combined duration once, as before, for naive datetimes.
    result = dt.add(days=days, seconds=seconds)  # type: ignore[arg-type]
    expected = datetime(2024, 4, 1, 4) + timedelta(days=days, seconds=seconds)

    assert result.isoformat() == expected.isoformat()
    assert result.tzinfo is None
