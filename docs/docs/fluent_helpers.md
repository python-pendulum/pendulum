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

>>> dt0 = pendulum.datetime(2013, 3, 31, 2, 30)
>>> print(dt0)
'2013-03-31T02:30:00+00:00'

>>> # Paris started DST on that exact day, so 2h30 local time doesn't exist. It immediately rolls over to 3h30. 
>>> dt = dt0.set(tz='Europe/Paris')
>>> print(dt)
'2013-03-31T03:30:00+02:00'

>>> dt = dt0.in_tz('Europe/Paris')
>>> print(dt)
'2013-03-31T04:30:00+02:00'

>>> dt = dt0.set(tz='Europe/Paris').set(tz='UTC')
>>> print(dt)
'2013-03-31T03:30:00+00:00'

>>> dt = dt0.in_tz('Europe/Paris').in_tz('UTC')
>>> print(dt)
'2013-03-31T02:30:00+00:00'
```
