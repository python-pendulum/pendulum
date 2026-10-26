# Attributes and Properties

Pendulum gives access to more attributes and properties than the default ``datetime`` class.

```python
>>> import pendulum

>>> dt = pendulum.parse('2012-09-05T23:26:11.123789')

# These properties specifically return integers
>>> dt.year
2012
>>> dt.month
9
>>> dt.day
5
>>> dt.hour
23
>>> dt.minute
26
>>> dt.second
11
>>> dt.microsecond
123789
>>> dt.day_of_week
<WeekDay.WEDNESDAY: 2>
>>> dt.day_of_year
249
>>> dt.week_of_month
1
>>> dt.week_of_year
36
>>> dt.days_in_month
30
>>> dt.timestamp()
1346887571.123789
>>> dt.float_timestamp
1346887571.123789
>>> dt.int_timestamp
1346887571

>>> pendulum.datetime(1975, 5, 21).age
41  # calculated vs now in the same tz
>>> dt.quarter
3

# Returns an int of seconds difference from UTC (+/- sign included)
>>> pendulum.from_timestamp(0).offset
0
>>> pendulum.from_timestamp(0, 'America/Toronto').offset
-18000

# Returns a float of hours difference from UTC (+/- sign included)
>>> pendulum.from_timestamp(0, 'America/Toronto').offset_hours
-5.0
>>> pendulum.from_timestamp(0, 'Australia/Adelaide').offset_hours
9.5

# Gets the timezone instance
>>> pendulum.now().timezone
>>> pendulum.now().tz

# Gets the timezone name
>>> pendulum.now().timezone_name

# Indicates if daylight savings time is on
>>> dt = pendulum.datetime(2012, 1, 1, tz='America/Toronto')
>>> dt.is_dst()
False
>>> dt = pendulum.datetime(2012, 9, 1, tz='America/Toronto')
>>> dt.is_dst()
True

# Indicates if the instance is in the same timezone as the local timezone
>>> pendulum.now().is_local()
True
>>> pendulum.now('Europe/London').is_local()
False

# Indicates if the instance is in the UTC timezone
>>> pendulum.now().is_utc()
False
>>> pendulum.now('Europe/London').is_local()
False
>>> pendulum.now('UTC').is_utc()
True
```
