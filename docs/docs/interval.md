# Interval

When you subtract a `DateTime` instance from another, or use the `diff()` method, it will return an `Interval` instance.
It inherits from the [Duration](#duration) class with the added benefit that it is aware of the
instances that generated it, so that it can give access to more methods and properties:

```python
>>> import pendulum

>>> start = pendulum.datetime(2000, 11, 20)
>>> end = pendulum.datetime(2016, 11, 5)

>>> interval = end - start

>>> interval.years
15
>>> interval.months
11
>>> interval.in_years()
15
>>> interval.in_months()
191

# Note that the weeks property
# will change compared to the Duration class
>>> interval.weeks
2 # 832 for the duration

# However the days property will still remain the same
# to keep the compatibility with the timedelta class
>>> interval.days
5829
```

Be aware that an interval, just like an duration, is compatible with the `timedelta` class regarding
its attributes. However, its custom attributes (like `remaining_days`) will be aware of any DST
transitions that might have occurred and adjust accordingly. Let's take an example:

```python
>>> import pendulum

>>> start = pendulum.datetime(2017, 3, 7, tz='America/Toronto')
>>> end = start.add(days=6)

>>> interval = end - start

# timedelta properties
>>> interval.days
5
>>> interval.seconds
82800

# interval properties
>>> interval.remaining_days
6
>>> interval.hours
0
>>> interval.remaining_seconds
0
```

!!!warning

    Due to their nature (fixed duration between two datetimes), most arithmetic operations will
    return a `Duration` instead of an `Interval`.

    ```python
    >>> import pendulum

    >>> dt1 = pendulum.datetime(2016, 8, 7, 12, 34, 56)
    >>> dt2 = dt1.add(days=6, seconds=34)
    >>> interval = pendulum.interval(dt1, dt2)
    >>> interval * 2
    Duration(weeks=1, days=5, minutes=1, seconds=8)
    ```


## Instantiation

You can create an instance by using the `interval()` helper:

```python

>>> import pendulum

>>> start = pendulum.datetime(2000, 1, 1)
>>> end = pendulum.datetime(2000, 1, 31)

>>> interval = pendulum.interval(start, end)
```

You can also make an inverted interval:

```python
>>> interval = pendulum.interval(end, start)
>>> interval.remaining_days
-2
```

If you have inverted dates but want to make sure that the interval is positive,
you should set the `absolute` keyword argument to `True`:

```python
>>> interval = pendulum.interval(end, start, absolute=True)
>>> interval.remaining_days
2
```

## Range

If you want to iterate over a interval, you can use the `range()` method:

```python
>>> import pendulum

>>> start = pendulum.datetime(2000, 1, 1)
>>> end = pendulum.datetime(2000, 1, 10)

>>> interval = pendulum.interval(start, end)

>>> for dt in interval.range('days'):
>>>     print(dt)

'2000-01-01T00:00:00+00:00'
'2000-01-02T00:00:00+00:00'
'2000-01-03T00:00:00+00:00'
'2000-01-04T00:00:00+00:00'
'2000-01-05T00:00:00+00:00'
'2000-01-06T00:00:00+00:00'
'2000-01-07T00:00:00+00:00'
'2000-01-08T00:00:00+00:00'
'2000-01-09T00:00:00+00:00'
'2000-01-10T00:00:00+00:00'
```

!!!note

    Supported units for `range()` are: `years`, `months`, `weeks`,
    `days`, `hours`, `minutes`, `seconds` and `microseconds`

You can pass a positive amount for the passed unit to control the length of the gap.
Zero or negative amounts raise `ValueError` when iteration starts. Inverted intervals
already iterate backwards, so their amount must also be positive:

```python
>>> for dt in interval.range('days', 2):
>>>     print(dt)

'2000-01-01T00:00:00+00:00'
'2000-01-03T00:00:00+00:00'
'2000-01-05T00:00:00+00:00'
'2000-01-07T00:00:00+00:00'
'2000-01-09T00:00:00+00:00'
```

You can also directly iterate over the `Interval` instance,
the unit will be `days` in this case:

```python
>>> for dt in interval:
>>>     print(dt)
```

You can check if a `DateTime` instance is inside a interval using the `in` keyword:

```python
>>> dt = pendulum.datetime(2000, 1, 4)
>>> dt in interval
True
```
