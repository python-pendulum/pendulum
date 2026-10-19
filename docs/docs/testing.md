# Testing

Pendulum provides a few helpers to help you control the flow of time in your tests. Note that
these helpers are only available if you opted in the `test` extra during [installation](#installation).

!!!warning
    If you are migrating from Pendulum 2, note that the `set_test_now()` and `test()`
    helpers have been removed.


## Relative time travel

You can travel in time relatively to the current time

```python
>>> import pendulum

>>> now = pendulum.now()
>>> pendulum.travel(minutes=5)
>>> pendulum.now().diff_for_humans(now)
"5 minutes after"
```

Note that once you've travelled in time the clock **keeps ticking**. If you prefer to stop the time completely
you can use the `freeze` parameter:

```python
>>> import pendulum

>>> now = pendulum.now()
>>> pendulum.travel(minutes=5, freeze=True)
>>> pendulum.now().diff_for_humans(now)
"5 minutes after"  # This will stay like this indefinitely
```


## Absolute time travel

Sometimes, you may want to place yourself at a specific point in time.
This is possible by using the `travel_to()` helper. This helper accepts a `DateTime` instance
that represents the point in time where you want to travel to.

```python
>>> import pendulum

>>> pendulum.travel_to(pendulum.yesterday())
```

Similarly to `travel`, it's important to remember that, by default, the time keeps ticking so, if you prefer
stopping the time, use the `freeze` parameter:

```python
>>> import pendulum

>>> pendulum.travel_to(pendulum.yesterday(), freeze=True)
```

Passing `freeze=True` also stops a clock that is already travelling. Once frozen,
subsequent calls to `travel()` or `travel_to()` keep the clock frozen, even when
`freeze` is omitted. Use `travel_back()` before starting a new ticking clock.

## Travelling back to the present

Using any of the travel helpers will keep you in the past, or future, until you decide
to travel back to the present time. To do so, you may use the `travel_back()` helper.

```python
>>> import pendulum

>>> now = pendulum.now()
>>> pendulum.travel(minutes=5, freeze=True)
>>> pendulum.now().diff_for_humans(now)
"5 minutes after"
>>> pendulum.travel_back()
>>> pendulum.now().diff_for_humans(now)
"a few seconds after"
```

However, it might be cumbersome to remember to travel back so, instead, you can use any of the helpers as a context
manager:

```python
>>> import pendulum

>>> now = pendulum.now()
>>> with pendulum.travel(minutes=5, freeze=True):
>>>     pendulum.now().diff_for_humans(now)
"5 minutes after"
>>> pendulum.now().diff_for_humans(now)
"a few seconds after"
```
