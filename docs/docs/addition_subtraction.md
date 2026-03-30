# Addition and Subtraction

To easily add and subtract time, you can use the `add()` and `subtract()`
methods.
Each method returns a new `DateTime` instance.

```python
>>> import pendulum

>>> dt = pendulum.datetime(2012, 1, 31)

>>> dt.to_datetime_string()
'2012-01-31 00:00:00'

>>> dt = dt.add(years=5)
'2017-01-31 00:00:00'
>>> dt = dt.add(years=1)
'2018-01-31 00:00:00'
>>> dt = dt.subtract(years=1)
'2017-01-31 00:00:00'
>>> dt = dt.subtract(years=5)
'2012-01-31 00:00:00'

>>> dt = dt.add(months=60)
'2017-01-31 00:00:00'
>>> dt = dt.add(months=1)
'2017-02-28 00:00:00'
>>> dt = dt.subtract(months=1)
'2017-01-28 00:00:00'
>>> dt = dt.subtract(months=60)
'2012-01-28 00:00:00'

>>> dt = dt.add(days=29)
'2012-02-26 00:00:00'
>>> dt = dt.add(days=1)
'2012-02-27 00:00:00'
>>> dt = dt.subtract(days=1)
'2012-02-26 00:00:00'
>>> dt = dt.subtract(days=29)
'2012-01-28 00:00:00'

>>> dt = dt.add(weeks=3)
'2012-02-18 00:00:00'
>>> dt = dt.add(weeks=1)
'2012-02-25 00:00:00'
>>> dt = dt.subtract(weeks=1)
'2012-02-18 00:00:00'
>>> dt = dt.subtract(weeks=3)
'2012-01-28 00:00:00'

>>> dt = dt.add(hours=24)
'2012-01-29 00:00:00'
>>> dt = dt.add(hours=1)
'2012-02-25 01:00:00'
>>> dt = dt.subtract(hours=1)
'2012-02-29 00:00:00'
>>> dt = dt.subtract(hours=24)
'2012-01-28 00:00:00'

>>> dt = dt.add(minutes=61)
'2012-01-28 01:01:00'
>>> dt = dt.add(minutes=1)
'2012-01-28 01:02:00'
>>> dt = dt.subtract(minutes=1)
'2012-01-28 01:01:00'
>>> dt = dt.subtract(minutes=24)
'2012-01-28 00:37:00'

>>> dt = dt.add(seconds=61)
'2012-01-28 00:01:01'
>>> dt = dt.add(seconds=1)
'2012-01-28 00:01:02'
>>> dt = dt.subtract(seconds=1)
'2012-01-28 00:01:01'
>>> dt = dt.subtract(seconds=61)
'2012-01-28 00:00:00'

>>> dt = dt.add(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
'2015-04-03 12:31:43'
>>> dt = dt.subtract(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
'2012-01-28 00:00:00'
```

!!!note

    Passing negative values to `add()` is also possible and will act exactly
    like `subtract()`
