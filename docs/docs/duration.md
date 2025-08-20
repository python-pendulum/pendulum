# Duration

The `Duration` class is inherited from the native `timedelta` class.
It has many improvements over the base class.

!!!note

    Even though, it inherits from the `timedelta` class, its behavior is slightly different.
    The more important to notice is that the native normalization does not happen, this is so that
    it feels more intuitive.

    ```python
    >>> import pendulum
    >>> import datetime

    >>> d1 = datetime.datetime(2012, 1, 1, 1, 2, 3, tzinfo=datetime.UTC)
    >>> d2 = datetime.datetime(2011, 12, 31, 22, 2, 3, tzinfo=datetime.UTC)
    >>> delta = d2 - d1
    >>> delta.days
    -1
    >>> delta.seconds
    75600

    >>> d1 = pendulum.datetime(2012, 1, 1, 1, 2, 3)
    >>> d2 = pendulum.datetime(2011, 12, 31, 22, 2, 3)
    >>> delta = d2 - d1
    >>> delta.days
    0
    >>> delta.hours
    -3
    ```

## Instantiation

To create a `Duration` instance, you can use the `duration()` helper:

```python
>>> import pendulum

>>> it = pendulum.duration(days=1177, seconds=7284, microseconds=1234)
```

!!!note

    Unlike the native `timedelta` class, durations support specifying
    years and months.

    ```python
    >>> import pendulum

    >>> it = pendulum.duration(years=2, months=3)
    ```

    However, to maintain compatibility, native methods and properties will
    make approximations:

    ```python
    >>> it.days
    820

    >>> it.total_seconds()
    70848000.0
    ```

## Properties and Duration Methods

The `Duration` class brings more properties than the default `days`, `seconds` and
`microseconds`.

```python
>>> import pendulum

>>> it = pendulum.duration(
...     years=2, months=3,
...     days=1177, seconds=7284, microseconds=1234
... )

>>> it.years
2
>>> it.months
3

# Weeks are based on the total of days
# It does not take into account years and months
>>> it.weeks
168

# Days, just like in timedelta, represents the total of days
# in the duration. If years and/or months are specified
# it will use an approximation
>>> it.days
1997

# If you want the remaining days not included in full weeks
>>> it.remaining_days
1

>>> # The remaining number in each unit
>>> it.hours
2
>>> it.minutes
1

# Seconds are, like days, a special case and the default
# property will return the whole value of remaining
# seconds just like the timedelta class for compatibility
>>> it.seconds
7284

# If you want the number of seconds not included
# in hours and minutes
>>> it.remaining_seconds
24

>>> it.microseconds
1234
```

If you want to get the duration in each supported unit
you can use the appropriate methods.

```python
# Each method returns a float like the native
# total_seconds() method
>>> it.total_weeks()
168.15490079569113

>>> it.total_days()
1177.0843055698379

>>> it.total_hours()
28250.02333367611

>>> it.total_minutes()
1695001.4000205665

>>> it.total_seconds()
101700084.001234
```

Similarly, the `in_xxx()` methods return the total duration in each
supported unit as a truncated integer.

```python
>>> it.in_weeks()
168

>>> it.in_days()
1997

>>> it.in_hours()
28250

>>> it.in_minutes()
1695001

>>> it.in_seconds()
101700084
```

It also has a handy `in_words()` method, which determines the duration representation when printed.

```python
>>> import pendulum

>>> pendulum.set_locale('fr')

>>> it = pendulum.duration(days=1177, seconds=7284, microseconds=1234)
>>> it.in_words()
'168 semaines 1 jour 2 heures 1 minute 24 secondes'

>>> print(it)
'168 semaines 1 jour 2 heures 1 minute 24 secondes'

>>> it.in_words(locale='de')
'168 Wochen 1 Tag 2 Stunden 1 Minute 24 Sekunden'
```
