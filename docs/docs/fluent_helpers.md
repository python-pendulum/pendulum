# Fluent helpers

Pendulum provides helpers that return a new instance with some attributes
modified compared to the original instance.
However, none of these helpers, with the exception of explicitly setting the
timezone, will change the timezone of the instance. Specifically,
setting the timestamp will not set the corresponding timezone to UTC.

```python
>>> import pendulum

>>> dt = pendulum.now()

>>> dt.set(year=1975, month=5, day=21).to_datetime_string()
'1975-05-21 13:45:18'

>>> dt.set(hour=22, minute=32, second=5).to_datetime_string()
'2016-11-16 22:32:05'
```

You can also use the `on()` and `at()` methods to change the date and the time
respectively

```python
>>> dt.on(1975, 5, 21).at(22, 32, 5).to_datetime_string()
'1975-05-21 22:32:05'

>>> dt.at(10).to_datetime_string()
'2016-11-16 10:00:00'

>>> dt.at(10, 30).to_datetime_string()
'2016-11-16 10:30:00'
```

You can also modify the timezone.

```python
>>> dt.set(tz='Europe/London')
```

Setting the timezone just modifies the timezone information without
making any conversion, while `in_timezone()` (or `in_tz()`)
converts the time in the appropriate timezone.

```python
>>> import pendulum

>>> dt = pendulum.datetime(2013, 3, 31, 2, 30)
>>> print(dt)
'2013-03-31T02:30:00+00:00'

>>> dt = dt.set(tz='Europe/Paris')
>>> print(dt)
'2013-03-31T03:30:00+02:00'

>>> dt = dt.in_tz('Europe/Paris')
>>> print(dt)
'2013-03-31T04:30:00+02:00'

>>> dt = dt.set(tz='Europe/Paris').set(tz='UTC')
>>> print(dt)
'2013-03-31T03:30:00+00:00'

>>> dt = dt.in_tz('Europe/Paris').in_tz('UTC')
>>> print(dt)
'2013-03-31T02:30:00+00:00'
```

## Replacing time attributes

`Time.replace()` preserves `fold` unless you specify a new value, matching
`datetime.time.replace()`. This keeps the selected occurrence of an ambiguous
time when changing other attributes.

```python
>>> clock = pendulum.Time(1, 30, tzinfo=pendulum.timezone('America/New_York'), fold=1)
>>> clock.replace(minute=45).fold
1
>>> clock.replace(fold=0).fold
0
```
