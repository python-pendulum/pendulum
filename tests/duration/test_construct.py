from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum

from pendulum.duration import AbsoluteDuration
from tests.conftest import assert_duration


def test_defaults():
    pi = pendulum.duration()
    assert_duration(pi, 0, 0, 0, 0, 0, 0, 0)


def test_years():
    pi = pendulum.duration(years=2)
    assert_duration(pi, years=2, weeks=0)
    assert pi.days == 730
    assert pi.total_seconds() == 63072000


def test_months():
    pi = pendulum.duration(months=3)
    assert_duration(pi, months=3, weeks=0)
    assert pi.days == 90
    assert pi.total_seconds() == 7776000


def test_weeks():
    pi = pendulum.duration(days=365)
    assert_duration(pi, weeks=52)

    pi = pendulum.duration(days=13)
    assert_duration(pi, weeks=1)


def test_days():
    pi = pendulum.duration(days=6)
    assert_duration(pi, 0, 0, 0, 6, 0, 0, 0)

    pi = pendulum.duration(days=16)
    assert_duration(pi, 0, 0, 2, 2, 0, 0, 0)


def test_hours():
    pi = pendulum.duration(seconds=3600 * 3)
    assert_duration(pi, 0, 0, 0, 0, 3, 0, 0)


def test_minutes():
    pi = pendulum.duration(seconds=60 * 3)
    assert_duration(pi, 0, 0, 0, 0, 0, 3, 0)

    pi = pendulum.duration(seconds=60 * 3 + 12)
    assert_duration(pi, 0, 0, 0, 0, 0, 3, 12)


def test_all():
    pi = pendulum.duration(
        years=2, months=3, days=1177, seconds=7284, microseconds=1000000
    )
    assert_duration(pi, 2, 3, 168, 1, 2, 1, 25)
    assert pi.days == 1997
    assert pi.seconds == 7285


def test_absolute_interval():
    pi = AbsoluteDuration(days=-1177, seconds=-7284, microseconds=-1000001)
    assert_duration(pi, 0, 0, 168, 1, 2, 1, 25)
    assert pi.microseconds == 1
    assert pi.invert


def test_invert():
    pi = pendulum.duration(days=1177, seconds=7284, microseconds=1000000)
    assert not pi.invert

    pi = pendulum.duration(days=-1177, seconds=-7284, microseconds=-1000000)
    assert pi.invert


def test_as_timedelta():
    pi = pendulum.duration(seconds=3456.123456)
    assert_duration(pi, 0, 0, 0, 0, 0, 57, 36, 123456)
    delta = pi.as_timedelta()
    assert isinstance(delta, timedelta)
    assert delta.total_seconds() == 3456.123456
    assert delta.seconds == 3456


def test_float_years_and_months():
    with pytest.raises(ValueError):
        pendulum.duration(years=1.5)

    with pytest.raises(ValueError):
        pendulum.duration(months=1.5)


def test_new_does_not_depend_on_total_seconds_override(monkeypatch):
    # __new__ must derive the duration's total from the underlying timedelta,
    # not from a (possibly overridden) total_seconds(). On PyPy, total_seconds()
    # is overridden to read _days/_seconds/... which are not populated yet during
    # __new__, which zeroed out full-day durations (issue #876).
    from pendulum.duration import Duration

    monkeypatch.setattr(Duration, "total_seconds", lambda self: 0.0)

    assert pendulum.duration(days=1)._total == 86400.0
    assert pendulum.duration(hours=23)._total == 82800.0
