from __future__ import annotations

from itertools import count
from time import sleep
from typing import TYPE_CHECKING

import pytest

import pendulum

from pendulum.testing.traveller import Traveller
from pendulum.utils._compat import PYPY


if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(autouse=True)
def setup() -> Generator[None, None, None]:
    pendulum.travel_back()

    yield

    pendulum.travel_back()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel() -> None:
    now = pendulum.now()

    pendulum.travel(minutes=5)

    assert pendulum.now().diff_for_humans(now) == "5 minutes after"


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel_with_frozen_time() -> None:
    pendulum.travel(minutes=5, freeze=True)

    now = pendulum.now()

    sleep(0.01)

    assert now == pendulum.now()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_travel_to() -> None:
    dt = pendulum.datetime(2022, 1, 19, tz="local")

    pendulum.travel_to(dt)

    assert pendulum.now().date() == dt.date()


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
def test_freeze() -> None:
    pendulum.freeze()

    pendulum.travel(minutes=5)

    assert pendulum.now() == pendulum.now()

    pendulum.travel_back()

    pendulum.travel(minutes=5)

    now = pendulum.now()

    sleep(0.01)

    assert now != pendulum.now()

    pendulum.freeze()

    assert pendulum.now() == pendulum.now()

    pendulum.travel_back()

    with pendulum.freeze():
        assert pendulum.now() == pendulum.now()

    now = pendulum.now()

    sleep(0.01)

    assert now != pendulum.now()


@pytest.fixture
def ticking_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    # Advance time-machine's real clock deterministically, without sleeping.
    ticks = count(1_700_000_000_000_000_000, 1_000_000_000)
    monkeypatch.setattr(
        "time_machine._time_machine.original_time_ns", lambda: next(ticks)
    )


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
@pytest.mark.parametrize("method", ["travel", "travel_to"])
@pytest.mark.parametrize("initial_freeze", [None, False, True])
@pytest.mark.parametrize("freeze", [False, True])
def test_travel_freeze_state(
    ticking_clock: None, method: str, initial_freeze: bool | None, freeze: bool
) -> None:
    if initial_freeze is not None:
        pendulum.travel_to(pendulum.datetime(2024, 1, 1, 12), freeze=initial_freeze)

    if method == "travel":
        pendulum.travel(days=2, freeze=freeze)
    else:
        pendulum.travel_to(pendulum.datetime(2024, 2, 1, 12), freeze=freeze)

    first = pendulum.now("UTC")
    second = pendulum.now("UTC")
    if freeze or initial_freeze:
        assert second == first
    else:
        assert second == first.add(seconds=1)

    if method == "travel_to":
        assert first == pendulum.datetime(2024, 2, 1, 12)


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
@pytest.mark.parametrize("method", ["travel", "travel_to"])
def test_freeze_after_repeated_travel(ticking_clock: None, method: str) -> None:
    target = pendulum.datetime(2024, 1, 1, 12)
    pendulum.travel_to(target)
    pendulum.travel(days=1)
    if method == "travel":
        pendulum.travel(days=1, freeze=True)
    else:
        pendulum.travel_to(target, freeze=True)

    frozen = pendulum.now("UTC")
    pendulum.travel(hours=2)
    assert pendulum.now("UTC") == frozen.add(hours=2)
    assert pendulum.now("UTC") == frozen.add(hours=2)
    pendulum.travel_to(target)
    assert pendulum.now("UTC") == target
    assert pendulum.now("UTC") == target

    pendulum.travel_back()
    pendulum.travel_to(target)
    assert pendulum.now("UTC") == target
    assert pendulum.now("UTC") == target.add(seconds=1)


@pytest.mark.skipif(PYPY, reason="Time travelling not available on PyPy")
@pytest.mark.parametrize("method", ["travel", "travel_to"])
def test_freeze_active_traveller_in_nested_context(
    ticking_clock: None, method: str
) -> None:
    outer_target = pendulum.datetime(2024, 1, 1, 12)
    inner_target = pendulum.datetime(2024, 2, 1, 12)
    with Traveller().travel_to(outer_target):
        with Traveller().travel_to(inner_target) as inner:
            if method == "travel":
                assert inner.travel(hours=2, freeze=True) is inner
            else:
                assert inner.travel_to(inner_target, freeze=True) is inner
            assert pendulum.now("UTC") == pendulum.now("UTC")

        first = pendulum.now("UTC")
        assert first.date() == outer_target.date()
        assert pendulum.now("UTC") == first.add(seconds=1)
