"""
tr custom locale file.
"""
from __future__ import annotations


translations = {
    # Relative time
    "ago": "{} önce",
    "from_now": "{} içinde",
    "after": "{0} sonra",
    "before": "{0} önce",
    # Ordinals
    "ordinal": {"one": ".", "two": ".", "few": ".", "other": "."},
    # Date formats
    "date_formats": {
        "LTS": "HH:mm:ss",
        "LT": "HH:mm",
        "L": "DD.MM.YYYY",
        "LL": "D MMMM YYYY",
        "LLL": "D MMMM YYYY HH:mm",
        "LLLL": "dddd, D MMMM YYYY HH:mm",
    },
}
