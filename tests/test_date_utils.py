import sys
import datetime
import unittest

from date_utils import get_min_time, get_max_time
from date_utils import get_date_boundaries
from date_utils import get_week_boundaries, get_month_boundaries
from date_utils import get_dates_between_range
from date_utils import get_week_start_dates_between_range
from date_utils import get_month_start_dates_between_range
from date_utils import get_years_between_range
from date_utils import convert_date_str_to_utc
from date_utils import convert_date_str_to_date
from date_utils import convert_date_to_local_date


class DateUtilsTestCase(unittest.TestCase):
    def test_min_date(self):
        today = datetime.datetime.today()
        expected = today.replace(hour=0, minute=0, second=0, microsecond=0)
        actual = get_min_time(today)

        self.assertEqual(actual, expected)

    def test_max_date(self):
        today = datetime.datetime.today()
        expected = today.replace(hour=23, minute=59, second=59,
                                 microsecond=999999)
        actual = get_max_time(today)

        self.assertEqual(actual, expected)

    def test_get_date_boundaries(self):
        dates = [
            datetime.datetime(2013, 9, 17)
        ]

        expected_boundaries = [
            (get_min_time(dates[0]), get_max_time(dates[0]))
        ]

        for index, date in enumerate(dates):
            expected = expected_boundaries[index]
            boundaries = get_date_boundaries(date=date)
            self.assertEqual(expected, boundaries)

    def test_get_week_boundaries(self):
        dates = [
            # Week 1
            datetime.date(2013, 9, 17),  # Tuesday
            datetime.date(2013, 9, 18),  # Wednesday
            datetime.date(2013, 9, 22),  # Sunday

            # Week 2
            datetime.date(2013, 9, 23),  # Monday
            datetime.date(2013, 9, 25),  # Wednesday
            datetime.date(2013, 9, 29),  # Sunday

            # Week 3
            datetime.date(2013, 9, 30),  # Monday
            datetime.date(2013, 10, 2),  # Wednesday
            datetime.date(2013, 10, 6),  # Sunday

        ]

        expected_boundaries = [
            # Week 1
            (get_min_time(datetime.datetime(2013, 9, 16)),
             get_max_time(datetime.datetime(2013, 9, 22))),

            # Week 2
            (get_min_time(datetime.datetime(2013, 9, 23)),
             get_max_time(datetime.datetime(2013, 9, 29))),

            # Week 3
            (get_min_time(datetime.datetime(2013, 9, 30)),
             get_max_time(datetime.datetime(2013, 10, 6))),
        ]

        for index, date in enumerate(dates):
            if index <= 2:
                expected = expected_boundaries[0]
            elif index > 2 and index <= 5:
                expected = expected_boundaries[1]
            else:
                expected = expected_boundaries[2]

            boundaries = get_week_boundaries(date=date)
            self.assertEqual(expected, boundaries)

    def test_get_month_boundaries(self):
        dates = [
            # Month 1
            datetime.date(2013, 9, 1),
            datetime.date(2013, 9, 18),
            datetime.date(2013, 9, 30),

            # Month 2
            datetime.date(2013, 10, 1),
            datetime.date(2013, 10, 20),
            datetime.date(2013, 10, 28),

            # Month 3
            datetime.date(2013, 12, 1),
            datetime.date(2013, 12, 20),
            datetime.date(2013, 12, 28),
        ]

        expected_boundaries = [
            # Month 1
            (get_min_time(datetime.datetime(2013, 9, 1)),
             get_max_time(datetime.datetime(2013, 9, 30))),

            # Month 2
            (get_min_time(datetime.datetime(2013, 10, 1)),
             get_max_time(datetime.datetime(2013, 10, 31))),

            # Month 3
            (get_min_time(datetime.datetime(2013, 12, 1)),
             get_max_time(datetime.datetime(2013, 12, 31))),
        ]

        for index, date in enumerate(dates):
            if index <= 2:
                expected = expected_boundaries[0]
            elif index > 2 and index <= 5:
                expected = expected_boundaries[1]
            else:
                expected = expected_boundaries[2]

            boundaries = get_month_boundaries(date=date)
            self.assertEqual(expected, boundaries)

    def test_get_dates_between_range(self):
        date_end = datetime.datetime.today()
        date_start = (date_end - datetime.timedelta(days=30))

        result_normal = get_dates_between_range(date_start=date_start,
                                                date_end=date_end,
                                                reverse=False)
        result_reversed = get_dates_between_range(date_start=date_start,
                                                  date_end=date_end,
                                                  reverse=True)

        self.assertEqual(len(result_normal), 31)
        self.assertEqual(result_normal[0], date_start)
        self.assertEqual(result_normal[1], (date_start +
                                            datetime.timedelta(days=1)))
        self.assertEqual(result_normal[29], (date_end -
                                             datetime.timedelta(days=1)))
        self.assertEqual(result_normal[30], date_end)

        self.assertEqual(len(result_reversed), 31)
        self.assertEqual(result_reversed[0], date_end)
        self.assertEqual(result_reversed[1], (date_end -
                                              datetime.timedelta(days=1)))
        self.assertEqual(result_reversed[29], (date_start +
                                               datetime.timedelta(days=1)))
        self.assertEqual(result_reversed[30], date_start)

    def test_get_week_start_dates_between_range(self):
        values = [
            # Doesn't span a single week
            (datetime.date(2013, 9, 2), datetime.date(2013, 9, 8)),
            # Spans a single week
            (datetime.date(2013, 9, 2), datetime.date(2013, 9, 9)),
            # Spans three weeks
            (datetime.date(2013, 9, 2), datetime.date(2013, 9, 23)),
        ]
        expected_values = [
            [],
            [datetime.date(2013, 9, 2)],
            [datetime.date(2013, 9, 2), datetime.date(2013, 9, 9),
             datetime.date(2013, 9, 16)],
        ]

        for args, expected in zip(values, expected_values):
            result = get_week_start_dates_between_range(*args)
            self.assertEqual(result, expected)

    def test_get_month_start_dates_between_range(self):
        values = [
            # Doesn't span a single month
            (datetime.date(2013, 9, 2), datetime.date(2013, 9, 28)),
            # Spans a single month
            (datetime.date(2013, 9, 2), datetime.date(2013, 10, 1)),
            # Spans multiple months
            (datetime.date(2013, 9, 2), datetime.date(2014, 1, 1)),
            # Spans multiple years
            (datetime.date(2011, 9, 2), datetime.date(2014, 1, 1)),

        ]
        expected_values = [
            [],
            [datetime.date(2013, 9, 1)],
            [datetime.date(2013, 9, 1), datetime.date(2013, 10, 1),
             datetime.date(2013, 11, 1), datetime.date(2013, 12, 1)],
            [datetime.date(2011, 9, 1), datetime.date(2011, 10, 1),
             datetime.date(2011, 11, 1), datetime.date(2011, 12, 1),
             datetime.date(2012, 1, 1), datetime.date(2012, 2, 1),
             datetime.date(2012, 3, 1), datetime.date(2012, 4, 1),
             datetime.date(2012, 5, 1), datetime.date(2012, 6, 1),
             datetime.date(2012, 7, 1), datetime.date(2012, 8, 1),
             datetime.date(2012, 9, 1), datetime.date(2012, 10, 1),
             datetime.date(2012, 11, 1), datetime.date(2012, 12, 1),
             datetime.date(2013, 1, 1), datetime.date(2013, 2, 1),
             datetime.date(2013, 3, 1), datetime.date(2013, 4, 1),
             datetime.date(2013, 5, 1), datetime.date(2013, 6, 1),
             datetime.date(2013, 7, 1), datetime.date(2013, 8, 1),
             datetime.date(2013, 9, 1), datetime.date(2013, 10, 1),
             datetime.date(2013, 11, 1), datetime.date(2013, 12, 1)]
        ]

        for args, expected in zip(values, expected_values):
            result = get_month_start_dates_between_range(*args)
            self.assertEqual(result, expected)

    def test_get_years_between_range(self):
        values = [
            # Single year
            (datetime.date(2013, 9, 2), datetime.date(2013, 9, 28)),
            # Multiple years
            (datetime.date(2010, 9, 2), datetime.date(2013, 10, 1)),
        ]
        expected_values = [
            [2013],
            [2010, 2011, 2012, 2013]
        ]

        for args, expected in zip(values, expected_values):
            result = get_years_between_range(*args)
            self.assertEqual(result, expected)

    def test_convert_date_str_to_utc_and_convert_date_to_local_date(self):
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'

        date_str1 = 'Wed, 9 Oct 2013 00:39:59 +0200'
        date_str2 = 'Mon, 09 Sep 2013 17:42:22 -0700'

        # convert_date_to_local_date
        date1_expected = '2013-10-09 00:39:59 +0200'
        date2_expected = '2013-09-09 17:42:22 -0700'

        date1 = convert_date_str_to_date(date_str=date_str1)
        date2 = convert_date_str_to_date(date_str=date_str2)

        self.assertEqual(date1.strftime(fmt), date1_expected)
        self.assertEqual(date2.strftime(fmt), date2_expected)

        # convert_date_str_to_utc
        date1_expected = '2013-10-08 22:39:59 UTC+0000'
        date2_expected = '2013-09-10 00:42:22 UTC+0000'

        date1 = convert_date_str_to_utc(date_str=date_str1)
        date2 = convert_date_str_to_utc(date_str=date_str2)

        self.assertEqual(date1.strftime(fmt), date1_expected)
        self.assertEqual(date2.strftime(fmt), date2_expected)

        # Convert back to original timezone
        timezone = 'Europe/Ljubljana'
        expected = '2013-10-09 00:39:59 CEST+0200'
        date_local = convert_date_to_local_date(date=date1, timezone=timezone)
        self.assertEqual(date_local.strftime(fmt), expected)

        timezone = 'US/Pacific'
        expected = '2013-09-09 17:42:22 PDT-0700'
        date_local = convert_date_to_local_date(date=date2, timezone=timezone)
        self.assertEqual(date_local.strftime(fmt), expected)

        # Convert to a different timezone
        timezone = 'US/Pacific'
        expected = '2013-10-08 15:39:59 PDT-0700'
        date_local = convert_date_to_local_date(date=date1, timezone=timezone)
        self.assertEqual(date_local.strftime(fmt), expected)

        timezone = 'Europe/Ljubljana'
        expected = '2013-09-10 02:42:22 CEST+0200'
        date_local = convert_date_to_local_date(date=date2, timezone=timezone)
        self.assertEqual(date_local.strftime(fmt), expected)


if __name__ == '__main__':
    sys.exit(unittest.main())
