# Difference

The `diff()` method returns an [Interval](#interval) instance that represents the total duration
between two `DateTime` instances. This interval can be then expressed in various units.
These interval methods always return *the total difference expressed* in the specified time requested.
All values are truncated and not rounded.

The `diff()` method has a default first parameter which is the `DateTime` instance to compare to,
or `None` if you want to use `now()`.
The 2nd parameter is optional and indicates if you want the return value to be the absolute value
or a relative value that might have a `-` (negative) sign if the passed in date
is less than the current instance.
This will default to `True`, return the absolute value.

```python
>>> import pendulum

>>> dt_ottawa = pendulum.datetime(2000, 1, 1, tz='America/Toronto')
>>> dt_vancouver = pendulum.datetime(2000, 1, 1, tz='America/Vancouver')

>>> dt_ottawa.diff(dt_vancouver).in_hours()
3
>>> dt_ottawa.diff(dt_vancouver, False).in_hours()
3
>>> dt_vancouver.diff(dt_ottawa, False).in_hours()
-3

>>> dt = pendulum.datetime(2012, 1, 31, 0)
>>> dt.diff(dt.add(months=1)).in_days()
29
>>> dt.diff(dt.subtract(months=1), False).in_days()
-31

>>> dt = pendulum.datetime(2012, 4, 30, 0)
>>> dt.diff(dt.add(months=1)).in_days()
30
>>> dt.diff(dt.add(weeks=1)).in_days()
7

>>> dt = pendulum.datetime(2012, 1, 1, 0)
>>> dt.diff(dt.add(seconds=59)).in_minutes()
0
>>> dt.diff(dt.add(seconds=60)).in_minutes()
1
>>> dt.diff(dt.add(seconds=119)).in_minutes()
1
>>> dt.diff(dt.add(seconds=120)).in_minutes()
2
```

Difference for Humans
---------------------

The `diff_for_humans()` method will add a phrase after the difference value relative
to the instance and the passed in instance. There are 4 possibilities:

* When comparing a value in the past to default now:
    * 1 hour ago
    * 5 months ago

* When comparing a value in the future to default now:
    * in 1 hour
    * in 5 months

* When comparing a value in the past to another value:
    * 1 hour before
    * 5 months before

* When comparing a value in the future to another value:
    * 1 hour after
    * 5 months after

You may also pass `True` as a 2nd parameter to remove the modifiers `ago`, `in`, etc.

```python
>>> import pendulum

# The most typical usage is for comments
# The instance is the date the comment was created
# and its being compared to default now()
>>> pendulum.now().subtract(days=1).diff_for_humans()
'1 day ago'

>>> pendulum.now().diff_for_humans(pendulum.now().subtract(years=1))
'1 year after'

>>> dt = pendulum.datetime(2011, 8, 1)
>>> dt.diff_for_humans(dt.add(months=1))
'1 month before'
>>> dt.diff_for_humans(dt.subtract(months=1))
'1 month after'

>>> pendulum.now().add(seconds=5).diff_for_humans()
'in a few seconds'

>>> pendulum.now().subtract(days=24).diff_for_humans()
'3 weeks ago'

>>> pendulum.now().subtract(days=24).diff_for_humans(absolute=True)
'3 weeks'
```

You can also change the locale of the string either globally by using `pendulum.set_locale('fr')`
before the `diff_for_humans()` call or specifically for the call by passing the `locale` keyword
argument. See the [Localization](#localization) section for more detail.

```python
>>> import pendulum

>>> pendulum.set_locale('de')
>>> pendulum.now().add(years=1).diff_for_humans()
'in 1 Jahr'
>>> pendulum.now().add(years=1).diff_for_humans(locale='fr')
'dans 1 an'
```
