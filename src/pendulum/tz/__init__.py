from __future__ import annotations

from functools import cache
from zoneinfo import available_timezones

from pendulum.tz.local_timezone import get_local_timezone
from pendulum.tz.local_timezone import set_local_timezone
from pendulum.tz.local_timezone import test_local_timezone
from pendulum.tz.timezone import UTC
from pendulum.tz.timezone import FixedTimezone
from pendulum.tz.timezone import Timezone


PRE_TRANSITION = "pre"
POST_TRANSITION = "post"
TRANSITION_ERROR = "error"

_tz_cache: dict[int, FixedTimezone] = {}


@cache
def timezones() -> set[str]:
    return available_timezones()


def fixed_timezone(offset: int) -> FixedTimezone:
    """
    Return a Timezone instance given its offset in seconds.
    """
    if offset in _tz_cache:
        return _tz_cache[offset]

    tz = FixedTimezone(offset)
    _tz_cache[offset] = tz

    return tz


def local_timezone() -> Timezone | FixedTimezone:
    """
    Return the local timezone.
    """
    return get_local_timezone()


__all__ = [
    "UTC",
    "FixedTimezone",
    "Timezone",
    "fixed_timezone",
    "get_local_timezone",
    "local_timezone",
    "set_local_timezone",
    "test_local_timezone",
    "timezones",
]
