# Timezones

Timezones are an important part of every datetime library, and `pendulum`
tries to provide an easy and accurate system to handle them properly.

!!!note

    The timezone system works best inside the `pendulum` ecosystem but
    can also be used with the standard ``datetime`` library with a few limitations.
    See [Using the timezone library directly](#using-the-timezone-library-directly).

## Listing available time zones

You can retrieve the available IANA time zone names using
`pendulum.timezones()`.

```python
>>> import pendulum

>>> zones = pendulum.timezones()
>>> "Europe/Paris" in zones
True
```

The function returns a `set[str]` of available IANA time zone names.

## Normalization

When you create a `DateTime` instance, the library will normalize it for the
given timezone to properly handle any transition that might have occurred.

```python
>>> import pendulum

>>> pendulum.datetime(2013, 3, 31, 2, 30, tz='Europe/Paris')
# 2:30 for the 31th of March 2013 does not exist
# so pendulum will return the actual time which is 3:30+02:00
'2013-03-31T03:30:00+02:00'

>>> pendulum.datetime(2013, 10, 27, 2, 30, tz='Europe/Paris')
# Here, 2:30 exists twice in the day so pendulum will
# assume that the transition already occurred
'2013-10-27T02:30:00+01:00'
```

You can, however, control the normalization behavior:

```python
>>> import pendulum

>>> pendulum.datetime(2013, 3, 31, 2, 30, 0, 0, tz='Europe/Paris',
                      dst_rule=pendulum.PRE_TRANSITION)
'2013-03-31T01:30:00+01:00'
>>> pendulum.datetime(2013, 10, 27, 2, 30, 0, 0, tz='Europe/Paris',
                      dst_rule=pendulum.PRE_TRANSITION)
'2013-10-27T02:30:00+02:00'

>>> pendulum.datetime(2013, 3, 31, 2, 30, 0, 0, tz='Europe/Paris',
                      dst_rule=pendulum.TRANSITION_ERROR)
# NonExistingTime: The datetime 2013-03-31 02:30:00 does not exist
>>> pendulum.datetime(2013, 10, 27, 2, 30, 0, 0, tz='Europe/Paris',
                      dst_rule=pendulum.TRANSITION_ERROR)
# AmbiguousTime: The datetime 2013-10-27 02:30:00 is ambiguous.
```

Note that it only affects instances at creation time. Shifting time around
transition times still behaves the same.

## Shifting time to transition

So, what happens when you add time to a `DateTime` instance and stumble upon
a transition time?
Well `pendulum`, provided with the context of the previous instance, will
adopt the proper behavior and apply the transition accordingly.

```python
>>> import pendulum

>>> dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999,
                           tz='Europe/Paris')
'2013-03-31T01:59:59.999999+01:00'
>>> dt = dt.add(microseconds=1)
'2013-03-31T03:00:00+02:00'
>>> dt.subtract(microseconds=1)
'2013-03-31T01:59:59.999999+01:00'

>>> dt = pendulum.datetime(2013, 10, 27, 2, 59, 59, 999999,
                           tz='Europe/Paris',
                           dst_rule=pendulum.PRE_TRANSITION)
'2013-10-27T02:59:59.999999+02:00'
>>> dt = dt.add(microseconds=1)
'2013-10-27T02:00:00+01:00'
>>> dt = dt.subtract(microseconds=1)
'2013-10-27T02:59:59.999999+02:00'
```

## Switching timezones

You can easily change the timezone of a `DateTime` instance
with the `in_timezone()` method.

!!!note

    You can also use the more concise ``in_tz()``

```python
>>> in_paris = pendulum.datetime(2016, 8, 7, 22, 24, 30, tz='Europe/Paris')
'2016-08-07T22:24:30+02:00'
>>> in_paris.in_timezone('America/New_York')
'2016-08-07T16:24:30-04:00'
>>> in_paris.in_tz('Asia/Tokyo')
'2016-08-08T05:24:30+09:00'
```

## Using the timezone library directly

!!!warning

    **You should avoid using the timezone library in Python < 3.6.**

    This is due to the fact that Pendulum relies heavily on the presence
    of the `fold` attribute which was introduced in Python 3.6.

    The reason it works inside the Pendulum ecosystem is that it
    backports the `fold` attribute in the `DateTime` class.

Like said in the introduction, you can use the timezone library
directly with standard `datetime` objects but with limitations, especially
when adding and subtracting time around transition times.

The value of the `fold` attribute will be used
by default to determine the transition rule.

```python
>>> from datetime import datetime
>>> from pendulum import timezone

>>> paris = timezone('Europe/Paris')
>>> dt = datetime(2013, 3, 31, 2, 30)
# By default, fold is set to 0
>>> dt = paris.convert(dt)
>>> dt.isoformat()
'2013-03-31T01:30:00+01:00'

>>> dt = datetime(2013, 3, 31, 2, 30, fold=1)
>>> dt = paris.convert(dt)
>>> dt.isoformat()
'2013-03-31T03:30:00+02:00'
```

Instead of relying on the `fold` attribute, you can use the `dst_rule`
keyword argument. This is especially useful if you want to raise errors
on non-existing and ambiguous times.

```python
>>> import pendulum

>>> dt = datetime(2013, 3, 31, 2, 30)
# By default, fold is set to 0
>>> dt = paris.convert(dt, dst_rule=pendulum.PRE_TRANSITION)
>>> dt.isoformat()
'2013-03-31T01:30:00+01:00'

>>> dt = paris.convert(dt, dst_rule=pendulum.POST_TRANSITION)
>>> dt.isoformat()
'2013-03-31T03:30:00+02:00'

>>> paris.convert(dt, dst_rule=pendulum.TRANSITION_ERROR)
# NonExistingTime: The datetime 2013-03-31 02:30:00 does not exist
```

This works as expected. However, whenever we add or subtract a `timedelta`
object, things get tricky.

```python
>>> from datetime import datetime, timedelta
>>> from pendulum import timezone

>>> dt = datetime(2013, 3, 31, 1, 59, 59, 999999)
>>> dt = paris.convert(dt)
>>> dt.isoformat()
'2013-03-31T01:59:59.999999+01:00'
>>> dt = dt + timedelta(microseconds=1)
>>> dt.isoformat()
'2013-03-31T02:00:00+01:00'
```

This is not what we expect. It should be `2013-03-31T03:00:00+02:00`.
It is actually easy to retrieve the proper datetime by using `convert()`
again.

```python
>>> dt = tz.convert(dt)
>>> dt.isoformat()
'2013-03-31T03:00:00+02:00'
```

You can also get a normalized `datetime` object
from a `Timezone` by using the `datetime()` method:

```python
>>> import pendulum

>>> tz = pendulum.timezone('Europe/Paris')
>>> dt = tz.datetime(2013, 3, 31, 2, 30)
>>> dt.isoformat()
'2013-03-31T03:30:00+02:00'
```
