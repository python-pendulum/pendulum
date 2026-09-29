# Instantiation

There are several different methods available to create a new `DateTime` instance.

First there is the main `datetime()` helper.

```python
>>> import pendulum

>>> dt = pendulum.datetime(2015, 2, 5)
>>> isinstance(dt, datetime)
True
>>> dt.timezone.name
'UTC'
```

`datetime()` sets the time to `00:00:00` if it's not specified,
and the timezone (the `tz` keyword argument) to `UTC`.
Otherwise it can be a `Timezone` instance or simply a string timezone value.

```python
>>> import pendulum

>>> pendulum.datetime(2015, 2, 5, tz='Europe/Paris')
>>> tz = pendulum.timezone('Europe/Paris')
>>> pendulum.datetime(2015, 2, 5, tz=tz)
```

!!!note

    Supported strings for timezones are the one provided
    by the [IANA time zone database](https://www.iana.org/time-zones).

    The special `local` string is also supported and will return your current timezone.

!!!warning

    The `tz` argument is keyword-only, unlike in version `1.x`

The `local()` helper is similar to `datetime()` but automatically sets the
timezone to the local timezone.

```python
>>> import pendulum

>>> dt = pendulum.local(2015, 2, 5)
>>> print(dt.timezone.name)
'America/Toronto'
```

!!!note

    `local()` is just an alias for `datetime(..., tz='local')`.

There is also the `now()` method.

```python
>>> import pendulum

>>> now = pendulum.now()

>>> now_in_london_tz = pendulum.now('Europe/London')
>>> now_in_london_tz.timezone_name
'Europe/London'
```

`now()` also accepts standard library `datetime.tzinfo` objects, including
`datetime.timezone.utc` and `zoneinfo.ZoneInfo`.

To accompany `now()`, a few other static instantiation helpers exist to create known instances.
The only thing to really notice here is that `today()`, `tomorrow()` and `yesterday()`,
besides behaving as expected, all accept a timezone parameter
and each has their time value set to `00:00:00`.

```python
>>> now = pendulum.now()
>>> print(now)
'2016-06-28T16:51:45.978473-05:00'

>>> today = pendulum.today()
>>> print(today)
'2016-06-28T00:00:00-05:00'

>>> tomorrow = pendulum.tomorrow('Europe/London')
>>> print(tomorrow)
'2016-06-29T00:00:00+01:00'

>>> yesterday = pendulum.yesterday()
>>> print(yesterday)
'2016-06-27T00:00:00-05:00'
```

Pendulum enforces timezone aware datetimes, and using them is the preferred and recommended way
of using the library. However, if you really need a **naive** `DateTime` object, the `naive()` helper
is there for you.

```python
>>> import pendulum

>>> naive = pendulum.naive(2015, 2, 5)
>>> naive.timezone
None
```

The next helper, `from_format()`, is similar to the native `datetime.strptime()` function
but uses custom tokens to create a `DateTime` instance.

```python
>>> dt = pendulum.from_format('1975-05-21 22', 'YYYY-MM-DD HH')
>>> print(dt)
'1975-05-21T22:00:00+00:00'
```

!!!note

    To see all the available tokens, you can check the [Formatter](#formatter) section.

It also accepts a `tz` keyword argument to specify the timezone:

```python
>>> dt = pendulum.from_format('1975-05-21 22', 'YYYY-MM-DD HH', tz='Europe/London')
'1975-05-21T22:00:00+01:00'
```

The final helper is for working with unix timestamps.
`from_timestamp()` will create a `DateTime` instance equal to the given timestamp
and will set the timezone as well or default it to `UTC`.

```python
>>> dt = pendulum.from_timestamp(-1)
>>> print(dt)
'1969-12-31T23:59:59+00:00'

>>> dt  = pendulum.from_timestamp(-1, tz='Europe/London')
>>> print(dt)
'1970-01-01T00:59:59+01:00'
```

Finally, if you find yourself inheriting a `datetime.datetime` instance,
you can create a `DateTime` instance via the `instance()` function.

```python
>>> dt = datetime(2008, 1, 1)
>>> p = pendulum.instance(dt)
>>> print(p)
'2008-01-01T00:00:00+00:00'
```
