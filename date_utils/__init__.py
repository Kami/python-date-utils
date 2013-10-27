# Licensed to Tomaz Muraus under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# Tomaz muraus licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import calendar
import time
from email.utils import parsedate_tz

import pytz


__all__ = [
    '__version__',
    'get_min_time',
    'get_max_time',
    'get_date_boundaries',
    'get_week_boundaries',
    'get_month_boundaries',
    'get_years_between_range',
    'parse_and_format_date',
    'convert_date_str_to_date',
    'convert_date_str_to_utc',
    'convert_date_to_local_date'
]

__version__ = '0.1.0'


class TZInfo(datetime.tzinfo):
    def __init__(self, offset):
        """
        :param offset: UTC offset in seconds.
        :type offset: ``int``
        """
        self.offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(seconds=self.offset)

    def tzname(self, dt):
        return ''

    def dst(self, dt):
        return datetime.timedelta(0)


def get_min_time(date):
    """
    Return minimum time for the provided date.
    Minimum time means hour, minute, second and microsecond are all zero.
    """
    if isinstance(date, datetime.date):
        date = datetime.datetime(date.year, date.month, date.day)

    min_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    return min_date


def get_max_time(date):
    """
    Return maximum time for the provided date.

    Maximum time means, hour, minute second and microsecond are at their
    maximum value.
    """
    if isinstance(date, datetime.date):
        date = datetime.datetime(date.year, date.month, date.day)

    max_date = date.replace(hour=23, minute=59, second=59,
                            microsecond=999999)
    return max_date


def get_date_boundaries(date):
    """
    Return boundaries (day_date_start, day_date_end) for the provided date.
    """
    min_date = get_min_time(date)
    max_date = get_max_time(date)

    return (min_date, max_date)


def get_week_boundaries(date):
    """
    Return week boundaries (week_date_start, week_date_end) for the provided
    date.
    """
    date_values = date.isocalendar()
    week_number = date_values[1]

    # Need to subtract 1 because strptime doesn't expect isoweek
    values = {'year': date.year, 'week': week_number - 1}
    result = time.strptime('%(year)s %(week)s 1' % (values), '%Y %W %w')

    date_min = datetime.datetime.fromtimestamp(time.mktime(result))
    date_max = date_min + datetime.timedelta(days=6)
    date_max = get_max_time(date_max)
    return (date_min, date_max)


def get_month_boundaries(date):
    """
    Return month boundaries (month_date_start, month_date_end) for the
    provided date.
    """
    year = date.year
    month = date.month

    _, max_day = calendar.monthrange(year, month)

    date_min = datetime.datetime(year, month, 1)
    date_min = get_min_time(date_min)
    date_max = datetime.datetime(year, month, max_day)
    date_max = get_max_time(date_max)

    return (date_min, date_max)


def get_week_start_dates_between_range(date_start, date_end):
    """
    Return a list of week start boundaries between the provided
    ranges.

    :param date_start: Start date.
    :type date_start: ``datetime.date``

    :param date_end: End date.
    :type date_end: ``datetime.date``

    :return: A list of ``datetime.date`` objects. Each date object day starts
             on Monday.
    :rtype: ``list``
    """
    min_date, _ = get_week_boundaries(date=date_start)
    min_date = min_date.date()

    difference_days = (date_end - min_date).days
    week_count = (difference_days / 7)

    dates = []

    if week_count == 0:
        # Doesn't span a single week
        return dates

    dates.append(min_date)

    for week_num in range(1, week_count):
        days = (week_num * 7)
        date = (min_date + datetime.timedelta(days=days))
        dates.append(date)

    return dates


def get_month_start_dates_between_range(date_start, date_end):
    """
    Return a list of month start boundaries between the provided
    ranges.

    :param date_start: Start date.
    :type date_start: ``datetime.date``

    :param date_end: End date.
    :type date_end: ``datetime.date``

    :return: A list of ``datetime.date`` objects. Each date object day starts
             with 1st.
    :rtype: ``list``
    """
    min_date, _ = get_month_boundaries(date=date_start)
    min_date = min_date.date()
    dates = get_dates_between_range(date_start=min_date, date_end=date_end)
    count = len(dates)

    result = []

    if date_start.month == date_end.month and date_start.year == date_end.year:
        return []

    for index, date in enumerate(dates):
        if date.day == 1 and index < (count - 1):
            result.append(date)

    return result


def get_years_between_range(date_start, date_end):
    """
    Return a list of years between the provided ranges inclusive of start and
    end year.

    :param date_start: Start date.
    :type date_start: ``datetime.date``

    :param date_end: End date.
    :type date_end: ``datetime.date``

    :rtype: ``list`` of ``int``
    """
    min_year = date_start.year
    max_year = date_end.year

    diff = (max_year - min_year)

    result = []

    for index in range(0, diff + 1):
        result.append(min_year + index)

    return result


def get_dates_between_range(date_start, date_end, reverse=False):
    """
    Return a list of date objects between the provided range in a daily
    increment including the start and end date. Dates are returned in the
    ascending order by default.

    :param date_start: Start date.
    :type date_start: ``datetime.date``

    :param date_end: End date.
    :type date_end: ``datetime.date``

    :param reverse: True to return values in the descending order.
    :type reverse: ``bool`

    :return: A list of ``datetime.date`` objects.
    :rtype: ``list``
    """
    difference_days = (date_end - date_start).days
    dates = []

    if reverse:
        values = range(0, difference_days)
    else:
        values = reversed(range(1, difference_days + 1))

    for value in values:
        date = (date_end - datetime.timedelta(days=value))
        dates.append(date)

    if reverse:
        dates.append(date_start)
    else:
        dates.append(date_end)

    return dates


def parse_and_format_date(value):
    """
    Try to parse a date in either UNIX timestamp or YYYY-mm-dd format.

    :param value: Date to parse.
    :type value: ``str`` or ``int``

    :rtype: ``datetime.date``
    """
    if isinstance(value, int) or value.isdigit():
        value = int(value)
        return datetime.datetime.fromtimestamp(value)
    else:
        return datetime.datetime.strptime(value, '%Y-%m-%d')


def convert_date_str_to_utc(date_str):
    """
    Convert date string in the following format
    "Wed, 9 Oct 2013 00:39:59 +0200" to UTC datetime object.

    :param date_str: Date in the following format:
                    "Wed, 9 Oct 2013 00:39:59 +0200"
    :type date_str: ``str``

    :rtype: ``datetime.datetime``
    """
    date = convert_date_str_to_date(date_str=date_str)
    date = convert_date_to_local_date(date=date, timezone='UTC')
    return date


def convert_date_str_to_date(date_str):
    """
    Convert date string to a time-zone aware datetime object.

    :param date_str: Date in the following format:
                    "Wed, 9 Oct 2013 00:39:59 +0200"
    :type date_str: ``str``

    :rtype: ``datetime.datetime``
    """
    parsed = parsedate_tz(date_str)
    date = datetime.datetime(*parsed[0:6])
    offset = parsed[-1]
    tzinfo = TZInfo(offset)
    date = date.replace(tzinfo=tzinfo)
    return date


def convert_date_to_local_date(date, timezone):
    """
    Convert datetime object to a local date in the provided timezone.

    :param date: Date to convert.
    :type date: ``datetime.datetime``

    :param timezone: Target timezone.
    :type timezone: ``str``

    :return: Date in the provided timezone.
    :rtype: ``datetime.datetime``
    """
    timezone = pytz.timezone(timezone)
    result = date.astimezone(timezone)
    return result
