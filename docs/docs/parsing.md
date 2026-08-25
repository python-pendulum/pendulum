# Parsing

The library natively supports the RFC 3339 format, most ISO 8601 formats and some other common formats.

```python
>>> import pendulum

>>> dt = pendulum.parse('1975-05-21T22:00:00')
>>> print(dt)
'1975-05-21T22:00:00+00:00

# You can pass a tz keyword to specify the timezone
>>> dt = pendulum.parse('1975-05-21T22:00:00', tz='Europe/Paris')
>>> print(dt)
'1975-05-21T22:00:00+01:00'

# Not ISO 8601 compliant but common
>>> dt = pendulum.parse('1975-05-21 22:00:00')
```

If you pass a non-standard or more complicated string, it will raise an exception, so it is advised to
use the `from_format()` helper instead.

However, if you want the library to fall back on the [dateutil](https://dateutil.readthedocs.io) parser,
you have to pass `strict=False`.

```python
>>> import pendulum

>>> dt = pendulum.parse('31-01-01')
Traceback (most recent call last):
...
ParserError: Unable to parse string [31-01-01]

>>> dt = pendulum.parse('31-01-01', strict=False)
>>> print(dt)
'2031-01-01T00:00:00+00:00'
```


## RFC 3339

| String                            | Output                                    |
| --------------------------------- | ------------------------------------------|
| 1996-12-19T16:39:57-08:00         | 1996-12-19T16:39:57-08:00                 |
| 1990-12-31T23:59:59Z              | 1990-12-31T23:59:59+00:00                 |

## ISO 8601

### Datetime

| String                            | Output                                    |
| --------------------------------- | ----------------------------------------- |
| 20161001T143028+0530              | 2016-10-01T14:30:28+05:30                 |
| 20161001T14                       | 2016-10-01T14:00:00+00:00                 |

### Date

| String                            | Output                                    |
| --------------------------------- | ----------------------------------------- |
| 2012                              | 2012-01-01T00:00:00+00:00                 |
| 2012-05-03                        | 2012-05-03T00:00:00+00:00                 |
| 20120503                          | 2012-05-03T00:00:00+00:00                 |
| 2012-05                           | 2012-05-01T00:00:00+00:00                 |

### Ordinal day

| String                             | Output                                    |
| ---------------------------------- | ----------------------------------------- |
| 2012-007                           | 2012-01-07T00:00:00+00:00                 |
| 2012007                            | 2012-01-07T00:00:00+00:00                 |

### Week number

| String                            | Output                                    |
| --------------------------------- | ----------------------------------------- |
| 2012-W05                          | 2012-01-30T00:00:00+00:00                 |
| 2012W05                           | 2012-01-30T00:00:00+00:00                 |
| 2012-W05-5                        | 2012-02-03T00:00:00+00:00                 |
| 2012W055                          | 2012-02-03T00:00:00+00:00                 |

### Time

When passing only time information the date will default to today.

| String                            | Output                                     |
| --------------------------------- | ------------------------------------------ |
| 00:00                             | 2016-12-17T00:00:00+00:00                  |
| 12:04:23                          | 2016-12-17T12:04:23+00:00                  |
| 120423                            | 2016-12-17T12:04:23+00:00                  |
| 12:04:23.45                       | 2016-12-17T12:04:23.450000+00:00           |

### Intervals

| String                                    | Output                                                 |
| ----------------------------------------- | ------------------------------------------------------ |
| 2007-03-01T13:00:00Z/2008-05-11T15:30:00Z | 2007-03-01T13:00:00+00:00 -> 2008-05-11T15:30:00+00:00 |
| 2008-05-11T15:30:00Z/P1Y2M10DT2H30M       | 2008-05-11T15:30:00+00:00 -> 2009-07-21T18:00:00+00:00 |
| P1Y2M10DT2H30M/2008-05-11T15:30:00Z       | 2007-03-01T13:00:00+00:00 -> 2008-05-11T15:30:00+00:00 |

!!!note

    You can pass the ``exact`` keyword argument to ``parse()`` to get the exact type
    that the string represents:

    ```python
    >>> import pendulum

    >>> pendulum.parse('2012-05-03', exact=True)
    Date(2012, 05, 03)

    >>> pendulum.parse('12:04:23', exact=True)
    Time(12, 04, 23)
    ```

## Typed helpers

Because `parse()` can return a `DateTime`, `Date`, `Time` or `Duration` depending on the
input, its return type is a union, which is awkward in type-checked code. If you know which
type you expect, you can use one of the typed helpers instead. Each one returns that single
type and raises a `ParserError` if the string represents something else.

```python
>>> import pendulum

>>> pendulum.parse_datetime('2012-05-03T12:04:23')
DateTime(2012, 5, 3, 12, 4, 23, tzinfo=Timezone('UTC'))

>>> pendulum.parse_datetime('P2Y3M4DT5H6M7S')
Traceback (most recent call last):
...
ParserError: Text 'P2Y3M4DT5H6M7S' does not represent a datetime, got Duration
```

`parse_date()` and `parse_time()` expect the string to represent that exact type, so pass
`exact=True` as you would to `parse()`:

```python
>>> pendulum.parse_date('2012-05-03', exact=True)
Date(2012, 5, 3)

>>> pendulum.parse_time('12:04:23', exact=True)
Time(12, 4, 23)

>>> pendulum.parse_duration('P2Y3M4DT5H6M7S')
Duration(years=2, months=3, days=4, hours=5, minutes=6, seconds=7)
```
