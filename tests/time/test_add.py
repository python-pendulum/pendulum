from __future__ import annotations

from datetime import timedelta

import pytest

import pendulum


def test_add_hours_positive():
    assert pendulum.time(12, 34, 56).add(hours=1).hour == 13


def test_add_hours_zero():
    assert pendulum.time(12, 34, 56).add(hours=0).hour == 12


def test_add_hours_negative():
    assert pendulum.time(12, 34, 56).add(hours=-1).hour == 11


def test_add_minutes_positive():
    assert pendulum.time(12, 34, 56).add(minutes=1).minute == 35


def test_add_minutes_zero():
    assert pendulum.time(12, 34, 56).add(minutes=0).minute == 34


def test_add_minutes_negative():
    assert pendulum.time(12, 34, 56).add(minutes=-1).minute == 33


def test_add_seconds_positive():
    assert pendulum.time(12, 34, 56).add(seconds=1).second == 57


def test_add_seconds_zero():
    assert pendulum.time(12, 34, 56).add(seconds=0).second == 56


def test_add_seconds_negative():
    assert pendulum.time(12, 34, 56).add(seconds=-1).second == 55


def test_add_timedelta():
    delta = timedelta(seconds=45, microseconds=123456)
    d = pendulum.time(3, 12, 15, 654321)

    d = d.add_timedelta(delta)
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777

    d = pendulum.time(3, 12, 15, 654321)

    d = d + delta
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_add_timedelta_with_days():
    delta = timedelta(days=3, seconds=45, microseconds=123456)
    d = pendulum.time(3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d.add_timedelta(delta)


@pytest.mark.parametrize("duration_type", [timedelta, pendulum.duration])
@pytest.mark.parametrize(
    "time_args, duration_args, expected_args",
    [
        (
            (3, 12, 15, 654321),
            {"seconds": 45, "microseconds": 123456},
            (3, 13, 0, 777777),
        ),
        ((12, 0), {}, (12, 0)),
        ((23, 59, 59, 999999), {"microseconds": 1}, (0, 0)),
        ((12, 0), {"hours": 23}, (11, 0)),
    ],
)
def test_reflected_addition(duration_type, time_args, duration_args, expected_args):
    value = pendulum.time(*time_args)
    delta = duration_type(**duration_args)
    expected = pendulum.time(*expected_args)

    assert value + delta == expected
    result = delta + value
    assert result == expected
    assert isinstance(result, pendulum.Time)


@pytest.mark.parametrize("days", [-1, 1])
def test_reflected_addition_rejects_days(days):
    value = pendulum.time(12, 0)
    delta = timedelta(days=days)

    with pytest.raises(TypeError):
        value + delta
    with pytest.raises(TypeError):
        delta + value


def test_reflected_addition_delegates_to_subclass():
    calls = []
    expected = pendulum.time(6, 0)

    class CustomTime(pendulum.Time):
        def __add__(self, other):
            calls.append(other)
            return expected

    delta = timedelta(minutes=5)
    assert delta + CustomTime(12, 0) is expected
    assert calls == [delta]


def test_addition_invalid_type():
    d = pendulum.time(3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d + 3

    with pytest.raises(TypeError):
        3 + d
