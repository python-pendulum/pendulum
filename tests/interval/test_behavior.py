from __future__ import annotations

import pickle
import copy

from datetime import timedelta

import pendulum


def test_pickle():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    p = pendulum.interval(dt1, dt2)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.interval(dt2, dt1)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.interval(dt2, dt1, True)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert


def test_comparison_to_timedelta():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    interval = dt2 - dt1

    assert interval < timedelta(days=4)


def test_equality_to_timedelta():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    interval = dt2 - dt1

    assert interval == timedelta(days=2)


def test_inequality():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)
    dt3 = pendulum.datetime(2016, 11, 22)

    interval1 = dt2 - dt1
    interval2 = dt3 - dt2
    interval3 = dt3 - dt1

    assert interval1 != interval2
    assert interval1 != interval3


def test_deepcopy():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    interval = dt2 - dt1

    interval2 = copy.deepcopy(interval)

    assert interval == interval2
    # make sure it's a deep copy
    assert interval is not interval2
    assert interval.start is not interval2.start
    assert interval.end is not interval2.end
