import unittest
from commands.command_spent import *
from unittest.mock import MagicMock


class TestSpent(unittest.TestCase):
    def test_get_date(self):
        self.assertEqual(get_date('today'), str(datetime.today().date())[:-3])
        self.assertEqual(get_date('2022-12'), '2022-12')
        self.assertEqual(get_date('january'), None)

    def test_validate_spent_parameters(self):
        executor = SpentCommandExecutor()
        self.assertEqual(
            {
                'start_date': '2022-12',
                'end_date': '2023-01',
                'category': 'takeaway'
            },
            executor.validate(['2022-12', '2023-01', 'takeaway'])
        )

        self.assertEqual(
            {
                'start_date': '2022-12',
                'end_date': '2023-01',
                'category': '$all'
            },
            executor.validate(['2022-12', '2023-01'])
        )

        self.assertEqual(
            {
                'start_date': '2022-12',
                'end_date': '2022-12',
                'category':  'takeaway'
            },
            executor.validate(['2022-12', 'takeaway'])
        )

        self.assertEqual(
            {
                'start_date': str(datetime.today().date())[:-3],
                'end_date': str(datetime.today().date())[:-3],
                'category': 'takeaway'
            },
            executor.validate(['takeaway'])
        )

        self.assertEqual(
            {
                'start_date': '2022-12',
                'end_date': '2022-12',
                'category': '$all'
            },
            executor.validate(['2022-12'])
        )

        self.assertEqual(
            {
                'start_date': (str(datetime.today().date()))[:-3],
                'end_date': (str(datetime.today().date()))[:-3],
                'category': '$all'
            },
            executor.validate([]))

        self.assertEqual(executor.validate(['2022-12', '2023-01', 'takeaway', 'coffee']), None)
        self.assertEqual(executor.validate(['takeaway', '2023-01', '2022-12']), None)
        self.assertEqual(executor.validate(['takeaway', '2023-01']), None)
        self.assertEqual(executor.validate(['2023-01', '2022-12', 'dog']), None)

    def test_command_execute(self):
        command = SpentCommandExecutor()

        class TestAdapter:
            pass
        adapter = TestAdapter()

        adapter.calculate_spent = MagicMock(return_value={'meat': '129', 'takeaway': '76'})
        self.assertEqual(
            'SPENT meat: 129 EUR, takeaway: 76 EUR, period: 2022-12 to 2023-02',
            command.execute(adapter, ['2022-12', '2023-02', '$each'])
        )

        adapter.calculate_spent = MagicMock(return_value=None)
        self.assertEqual(
            'FAILED to calculate SPENT',
            command.execute(adapter, ['2022-12', '2023-02', '$each'])
        )


if __name__ == '__main__':
    unittest.main()
