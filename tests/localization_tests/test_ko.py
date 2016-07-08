# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class KoTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'ko'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('1 초 전', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('2 초 전', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('1 분 전', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('2 분 전', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('1 시간 전', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('2 시간 전', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('1 일 전', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('2 일 전', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('1 주일 전', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('2 주일 전', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('1 개월 전', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('2 개월 전', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('1 년 전', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('2 년 전', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('1 초 후', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 초 뒤', d.diff_for_humans(d2))
            self.assertEqual('1 초 앞', d2.diff_for_humans(d))

            self.assertEqual('1 초', d.diff_for_humans(d2, True))
            self.assertEqual('2 초', d2.diff_for_humans(d.add_second(), True))
