import unittest
from date_utils import get_month_today
from date_utils import get_date_today
from date_utils import months_spent
from freezegun import freeze_time


class DateToday(unittest.TestCase):
    def test_get_date_today(self):
        with freeze_time("2022-02-22"):
            self.assertEqual("2022-02", get_month_today())

        with freeze_time("2023-12-22"):
            self.assertEqual("2023-12", get_month_today())

        with freeze_time("1922-06-22"):
            self.assertEqual("1922-06", get_month_today())

    def test_get_day_today(self):
        with freeze_time("2023-04-22 20:03:30.638762"):
            self.assertEqual("2023-04-22", get_date_today())

        with freeze_time("2021-05-12 12:03:30.9"):
            self.assertEqual("2021-05-12", get_date_today())


class MonthsSpent(unittest.TestCase):
    def test_months_spent(self):
        self.assertEqual(months_spent("2022-11", "2023-02"), ["2022-11", "2022-12", "2023-01", "2023-02"])
        self.assertEqual(months_spent("2022-05", "2022-08"), ["2022-05", "2022-06", "2022-07", "2022-08"])


if __name__ == "__main__":
    unittest.main()
