from __future__ import annotations

import typing as t

from pendulum.locales.locale import Locale


if t.TYPE_CHECKING:
    from pendulum import Duration

DAYS_THRESHOLD_FOR_HALF_WEEK = 3
DAYS_THRESHOLD_FOR_HALF_MONTH = 15
MONTHS_THRESHOLD_FOR_HALF_YEAR = 6

HOURS_IN_NEARLY_A_DAY = 22
DAYS_IN_NEARLY_A_MONTH = 27
MONTHS_IN_NEARLY_A_YEAR = 11

DAYS_OF_WEEK = 7
SECONDS_OF_MINUTE = 60
FEW_SECONDS_MAX = 10

KEY_FUTURE = ".future"
KEY_PAST = ".past"
KEY_AFTER = ".after"
KEY_BEFORE = ".before"


class DifferenceFormatter:
    """
    Handles formatting differences in text.
    """

    def __init__(self, locale: str = "en") -> None:
        self._locale = Locale.load(locale)

    def format(
        self,
        diff: Duration,
        is_now: bool = True,
        absolute: bool = False,
        locale: str | Locale | None = None,
    ) -> str:
        """
        Formats a difference.

        :param diff: The difference to format
        :param is_now: Whether the difference includes now
        :param absolute: Whether it's an absolute difference or not
        :param locale: The locale to use
        """
        locale = self._locale if locale is None else Locale.load(locale)

        if diff.years > 0:
            unit = "year"
            count = diff.years

            if diff.months > MONTHS_THRESHOLD_FOR_HALF_YEAR:
                count += 1
        elif (diff.months == MONTHS_IN_NEARLY_A_YEAR) and (
            (diff.weeks * DAYS_OF_WEEK + diff.remaining_days)
            > DAYS_THRESHOLD_FOR_HALF_MONTH
        ):
            unit = "year"
            count = 1
        elif diff.months > 0:
            unit = "month"
            count = diff.months

            if (
                diff.weeks * DAYS_OF_WEEK + diff.remaining_days
            ) >= DAYS_IN_NEARLY_A_MONTH:
                count += 1
        elif diff.weeks > 0:
            unit = "week"
            count = diff.weeks

            if diff.remaining_days > DAYS_THRESHOLD_FOR_HALF_WEEK:
                count += 1
        elif diff.remaining_days > 0:
            unit = "day"
            count = diff.remaining_days

            if diff.hours >= HOURS_IN_NEARLY_A_DAY:
                count += 1
        elif diff.hours > 0:
            unit = "hour"
            count = diff.hours
        elif diff.minutes > 0:
            unit = "minute"
            count = diff.minutes
        elif FEW_SECONDS_MAX < diff.remaining_seconds < SECONDS_OF_MINUTE:
            unit = "second"
            count = diff.remaining_seconds
        else:
            # We check if the "a few seconds" unit exists
            time = locale.get("custom.units.few_second")
            if time is not None:
                if absolute:
                    return t.cast("str", time)

                key = "custom"
                is_future = diff.invert
                if is_now:
                    if is_future:
                        key += ".from_now"
                    else:
                        key += ".ago"
                else:
                    if is_future:
                        key += KEY_AFTER
                    else:
                        key += KEY_BEFORE

                return t.cast("str", locale.get(key).format(time))
            else:
                unit = "second"
                count = diff.remaining_seconds
        if count == 0:
            count = 1
        if absolute:
            key = f"translations.units.{unit}"
        else:
            is_future = diff.invert
            if is_now:
                # Relative to now, so we can use
                # the CLDR data
                key = f"translations.relative.{unit}"

                if is_future:
                    key += KEY_FUTURE
                else:
                    key += KEY_PAST
            else:
                # Absolute comparison
                # So we have to use the custom locale data

                # Checking for special pluralization rules
                key = "custom.units_relative"
                if is_future:
                    key += f".{unit}{KEY_FUTURE}"
                else:
                    key += f".{unit}{KEY_PAST}"

                trans = locale.get(key)
                if not trans:
                    # No special rule
                    key = f"translations.units.{unit}.{locale.plural(count)}"
                    time = locale.get(key).format(count)
                else:
                    time = trans[locale.plural(count)].format(count)

                key = "custom"
                if is_future:
                    key += KEY_AFTER
                else:
                    key += KEY_BEFORE

                return t.cast("str", locale.get(key).format(time))

        key += f".{locale.plural(count)}"

        return t.cast("str", locale.get(key).format(count))
