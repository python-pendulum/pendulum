from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import pytest

import pendulum

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
