from __future__ import annotations

import concurrent.futures

import pendulum


ITERATIONS = 200
WORKERS = 8


def _run_parallel(fn, *args):
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = [pool.submit(fn, *args) for _ in range(ITERATIONS)]
        return [f.result() for f in futures]


def test_parse_iso8601_threaded():
    results = _run_parallel(pendulum.parse, "2024-01-15T10:30:00+00:00")
    expected = results[0]
    assert all(r == expected for r in results)


def test_now_threaded():
    results = _run_parallel(pendulum.now)
    assert all(isinstance(r, pendulum.DateTime) for r in results)


def test_duration_threaded():
    def make_duration():
        return pendulum.duration(years=1, months=2, days=3)

    results = _run_parallel(make_duration)
    assert all(r.years == 1 and r.months == 2 for r in results)


def test_diff_threaded():
    dt1 = pendulum.datetime(2024, 1, 1)
    dt2 = pendulum.datetime(2024, 6, 15)

    def compute_diff():
        return dt1.diff(dt2)

    results = _run_parallel(compute_diff)
    expected = results[0]
    assert all(r.in_days() == expected.in_days() for r in results)


def test_format_threaded():
    dt = pendulum.datetime(2024, 1, 15, 10, 30, 0)

    def format_dt():
        return dt.format("YYYY-MM-DD HH:mm:ss")

    results = _run_parallel(format_dt)
    assert all(r == "2024-01-15 10:30:00" for r in results)
