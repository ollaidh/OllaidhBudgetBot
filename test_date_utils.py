import unittest
from date_utils import get_date_today
from freezegun import freeze_time


class DateToday(unittest.TestCase):
    def test_get_date_today(self):
        with freeze_time('2022-02-22'):
            self.assertEqual('2022-02', get_date_today())

        with freeze_time('2023-12-22'):
            self.assertEqual('2023-12', get_date_today())

        with freeze_time('1922-06-22'):
            self.assertEqual('1922-06', get_date_today())


if __name__ == '__main__':
    unittest.main()
