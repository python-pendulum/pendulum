# -*- coding: utf-8 -*-

import re
import copy

from datetime import datetime
from dateutil import parser

from .exceptions import ParserError


class Parser(object):
    """
    Parser which parses common formats (like RFC3339 and ISO8601).
    """

    COMMON = re.compile(
        # Date (optional)
        '^'
        '(?P<date>'
        '    (?P<classic>'  # Classic date (YYYY-MM-DD) or ordinal (YYYY-DDD)
        '        (?P<year>\d{4})'  # Year
        '        (?P<monthday>'
        '            (?P<monthsep>[-/:])?(?P<month>\d{2})'  # Month (optional)
        '            ((?P<daysep>[-/:])?(?P<day>\d{1,2}))?'  # Day (optional)
        '        )?'
        '    )'
        '    |'
        '    (?P<isocalendar>'  # Calendar date (2016-W05 or 2016-W05-5)
        '        (?P<isoyear>\d{4})'  # Year
        '        -?'  # Separator (optional)
        '        W'  # W separator
        '        (?P<isoweek>\d{2})'  # Week number
        '        -?'  # Separator (optional)
        '        (?P<isoweekday>\d)?'  # Weekday (optional)
        '    )'
        ')?'

        # Time (optional)
        '(?P<time>'
        '    (?P<timesep>T|\ )?'  # Separator (T or space)
        '    (?P<hour>\d{1,2}):?(?P<minute>\d{1,2})?:?(?P<second>\d{1,2})?'  # HH:mm:ss (optional mm and ss)
        # Subsecond part (optional)
        '    (?P<subsecondsection>'
        '        (?:\.|,)'  # Subsecond separator (optional)
        '        (?P<subsecond>\d{1,9})'  # Subsecond
        '    )?'
        # Timezone offset
        '    (?P<tz>'
        '        (?:-|\+)\d{2}:?(?:\d{2})?|Z'  # Offset (+HH:mm or +HHmm or +HH or Z)
        '    )?'
        ')?'
        '$',
        re.VERBOSE
    )

    DEFAULT_OPTIONS = {
        'day_first': False,
        'year_first': True,
        'strict': False,
        'now': None
    }

    def __init__(self, **options):
        self._options = copy.copy(self.DEFAULT_OPTIONS)
        self._options.update(options)

    def is_strict(self):
        return self._options['strict']

    def now(self):
        return self._options['now'] or datetime.now()

    def parse_common(self, text):
        """
        Tries to parse the string as a common datetime format.

        :param text: The string to parse.
        :type text: str

        :rtype: dict or None
        """
        m = self.COMMON.match(text)
        parsed = {}
        ambiguous_date = False
        has_date = False

        if m:
            if m.group('date'):
                # A date has been specified
                has_date = True

                if m.group('isocalendar'):
                    # We have a ISO 8601 string defined
                    # by week number
                    try:
                        date = self._get_iso_8601_week(
                            m.group('isoyear'),
                            m.group('isoweek'),
                            m.group('isoweekday')
                        )
                    except ValueError:
                        raise ParserError('Invalid date string: {}'.format(text))

                    year = date['year']
                    month = date['month']
                    day = date['day']
                else:
                    # We have a classic date representation
                    year = int(m.group('year'))

                    if not m.group('monthday'):
                        # No month and day
                        month = 1
                        day = 1
                    else:
                        if m.group('month') and m.group('day'):
                            # Month and day
                            if not m.group('daysep') and len(m.group('day')) == 1:
                                # Ordinal day
                                dt = datetime.strptime(
                                    '{}-{}'.format(year, m.group('month') + m.group('day')),
                                    '%Y-%j'
                                )
                                month = dt.month
                                day = dt.day
                            elif self._options['day_first']:
                                month = int(m.group('day'))
                                day = int(m.group('month'))
                            else:
                                month = int(m.group('month'))
                                day = int(m.group('day'))
                        else:
                            # Only month
                            if not m.group('monthsep'):
                                # The date looks like 201207
                                # which is invalid for a date
                                # But it might be a time in the form hhmmss
                                ambiguous_date = True

                            month = int(m.group('month'))
                            day = 1

                parsed.update({
                    'year': year,
                    'month': month,
                    'day': day,
                })

            if not m.group('time'):
                # No time has been specified
                if ambiguous_date:
                    # We can "safely" assume that the ambiguous date
                    # was actually a time in the form hhmmss
                    hhmmss = '{}{:0>2}'.format(
                        str(parsed['year']),
                        str(parsed['month'])
                    )

                    return {
                        'hour': int(hhmmss[:2]),
                        'minute': int(hhmmss[2:4]),
                        'second': int(hhmmss[4:]),
                        'subsecond': 0
                    }

                return parsed

            if ambiguous_date:
                raise ParserError('Invalid date string: {}'.format(text))

            if has_date and not m.group('timesep'):
                raise ParserError('Invalid date string: {}'.format(text))

            parsed.update({
                'hour': 0,
                'minute': 0,
                'second': 0,
                'subsecond': 0,
                'offset': None
            })

            # Grabbing hh:mm:ss
            parsed['hour'] = int(m.group('hour'))

            if m.group('minute'):
                parsed['minute'] = int(m.group('minute'))

            if m.group('second'):
                parsed['second'] = int(m.group('second'))

            # Grabbing subseconds, if any
            if m.group('subsecondsection'):
                parsed['subsecond'] = int('{:0<9}'.format(m.group('subsecond')))

            # Grabbing timezone, if any
            tz = m.group('tz')
            if tz:
                if tz == 'Z':
                    offset = 0
                else:
                    negative = True if tz.startswith('-') else False
                    tz = tz[1:]
                    if ':' not in tz:
                        if len(tz) == 2:
                            tz = '{}00'.format(tz)

                        off_hour = tz[0:2]
                        off_minute = tz[2:4]
                    else:
                        off_hour, off_minute = tz.split(':')

                    offset = ((int(off_hour) * 60) + int(off_minute)) * 60

                    if negative:
                        offset = -1 * offset

                parsed['offset'] = offset

            return parsed

    def _get_iso_8601_week(self, year, week, weekday):
        if not weekday:
            weekday = '1'

        fmt = '%YW%W%w'
        string = '{}W{}{}'.format(year, week, weekday)

        dt = datetime.strptime(string, fmt)

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
        }

    def parse(self, text):
        """
        Parses a string with the given options.

        :param text: The string to parse.
        :type text: str

        :rtype: dict
        """
        return self.normalize(self._parse(text))

    def normalize(self, parsed):
        """
        Normalizes the parsed element.

        :param parsed: The parsed elements.
        :type parsed: dict

        :rtype: dict
        """
        if self.is_strict():
            return parsed

        now = self.now()
        default = {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': 0,
            'minute': 0,
            'second': 0,
            'subsecond': 0,
            'offset': None
        }

        default.update(parsed)

        return default

    def _parse(self, text):
        parsed = self.parse_common(text)
        if parsed:
            return parsed

        # We couldn't parse the string
        # so we fallback on the dateutil parser
        try:
            dt = parser.parse(
                text,
                dayfirst=self._options['day_first'],
                yearfirst=self._options['year_first']
            )
        except ValueError:
            raise ParserError('Invalid date string: {}'.format(text))

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'subsecond': dt.microsecond * 1000,
            'offset': dt.utcoffset().total_seconds() if dt.tzinfo else None,
        }
