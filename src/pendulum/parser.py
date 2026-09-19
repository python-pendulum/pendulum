from __future__ import annotations

import datetime
import os
import typing as t

import pendulum

from pendulum.duration import Duration
from pendulum.parsing import _Interval
from pendulum.parsing import parse as base_parse
from pendulum.parsing.exceptions import ParserError
from pendulum.tz.timezone import UTC


if t.TYPE_CHECKING:
    from pendulum.date import Date
    from pendulum.datetime import DateTime
    from pendulum.interval import Interval
    from pendulum.time import Time

with_extensions = os.getenv("PENDULUM_EXTENSIONS", "1") == "1"

try:
    if not with_extensions:
        raise ImportError()

    from pendulum._pendulum import Duration as RustDuration
except ImportError:
    RustDuration = None  # type: ignore[assignment,misc]


def parse(text: str, **options: t.Any) -> Date | Time | DateTime | Duration:
    # Use the mock now value if it exists
    options["now"] = options.get("now")

    return _parse(text, **options)


def parse_datetime(text: str, **options: t.Any) -> DateTime:
    """Parse a string and return a ``DateTime``.

    Accepts the same options as ``parse()`` but raises a ``ParserError`` if the
    string represents something else (a date, a time, a duration, ...).
    """
    parsed = parse(text, **options)
    if not isinstance(parsed, pendulum.DateTime):
        raise _wrong_type(text, "a datetime", parsed)

    return parsed


def parse_date(text: str, **options: t.Any) -> Date:
    """Parse a string and return a ``Date``.

    Accepts the same options as ``parse()`` but raises a ``ParserError`` if the
    string represents something else. Note that ``parse()`` yields a ``DateTime``
    for a date string unless ``exact=True`` is passed.
    """
    parsed = parse(text, **options)
    # DateTime is a subclass of Date, so a datetime must not pass as a date.
    if not isinstance(parsed, pendulum.Date) or isinstance(parsed, pendulum.DateTime):
        raise _wrong_type(text, "a date", parsed)

    return parsed


def parse_time(text: str, **options: t.Any) -> Time:
    """Parse a string and return a ``Time``.

    Accepts the same options as ``parse()`` but raises a ``ParserError`` if the
    string represents something else. Note that ``parse()`` yields a ``DateTime``
    for a time string unless ``exact=True`` is passed.
    """
    parsed = parse(text, **options)
    if not isinstance(parsed, pendulum.Time):
        raise _wrong_type(text, "a time", parsed)

    return parsed


def parse_duration(text: str, **options: t.Any) -> Duration:
    """Parse a string and return a ``Duration``.

    Accepts the same options as ``parse()`` but raises a ``ParserError`` if the
    string represents something else.
    """
    parsed = parse(text, **options)
    # Interval is a subclass of Duration, so an interval must not pass as one.
    if not isinstance(parsed, Duration) or isinstance(parsed, pendulum.Interval):
        raise _wrong_type(text, "a duration", parsed)

    return parsed


def _wrong_type(text: str, expected: str, parsed: object) -> ParserError:
    return ParserError(
        f"Text '{text}' does not represent {expected}, got {type(parsed).__name__}"
    )


def _parse(
    text: str, **options: t.Any
) -> Date | DateTime | Time | Duration | Interval[DateTime]:
    """
    Parses a string with the given options.

    :param text: The string to parse.
    """
    # Handling special cases
    if text == "now":
        return pendulum.now(tz=options.get("tz", UTC))

    parsed = base_parse(text, **options)

    if isinstance(parsed, datetime.datetime):
        return pendulum.datetime(
            parsed.year,
            parsed.month,
            parsed.day,
            parsed.hour,
            parsed.minute,
            parsed.second,
            parsed.microsecond,
            tz=parsed.tzinfo or options.get("tz", UTC),
        )

    if isinstance(parsed, datetime.date):
        return pendulum.date(parsed.year, parsed.month, parsed.day)

    if isinstance(parsed, datetime.time):
        return pendulum.time(
            parsed.hour, parsed.minute, parsed.second, parsed.microsecond
        )

    if isinstance(parsed, _Interval):
        if parsed.duration is not None:
            duration = parsed.duration

            if parsed.start is not None:
                dt = pendulum.instance(parsed.start, tz=options.get("tz", UTC))

                return pendulum.interval(
                    dt,
                    dt.add(
                        years=duration.years,
                        months=duration.months,
                        weeks=duration.weeks,
                        days=duration.remaining_days,
                        hours=duration.hours,
                        minutes=duration.minutes,
                        seconds=duration.remaining_seconds,
                        microseconds=duration.microseconds,
                    ),
                )

            dt = pendulum.instance(
                t.cast("datetime.datetime", parsed.end), tz=options.get("tz", UTC)
            )

            return pendulum.interval(
                dt.subtract(
                    years=duration.years,
                    months=duration.months,
                    weeks=duration.weeks,
                    days=duration.remaining_days,
                    hours=duration.hours,
                    minutes=duration.minutes,
                    seconds=duration.remaining_seconds,
                    microseconds=duration.microseconds,
                ),
                dt,
            )

        return pendulum.interval(
            pendulum.instance(
                t.cast("datetime.datetime", parsed.start), tz=options.get("tz", UTC)
            ),
            pendulum.instance(
                t.cast("datetime.datetime", parsed.end), tz=options.get("tz", UTC)
            ),
        )

    if isinstance(parsed, Duration):
        return parsed

    if RustDuration is not None and isinstance(parsed, RustDuration):
        return pendulum.duration(
            years=parsed.years,
            months=parsed.months,
            weeks=parsed.weeks,
            days=parsed.days,
            hours=parsed.hours,
            minutes=parsed.minutes,
            seconds=parsed.seconds,
            microseconds=parsed.microseconds,
        )

    raise NotImplementedError
