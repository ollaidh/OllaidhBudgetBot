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

        adapter.calculate_spent = MagicMock(return_value={'meat': 129.111111111, 'takeaway': 76.2})
        self.assertEqual(
            f'SPENT STATISTICS:\nperiod: 2022-12 to 2023-02\nmeat: 129.1 {chr(8364)}\ntakeaway: 76.2 {chr(8364)}\n',
            command.execute(adapter, ['2022-12', '2023-02', '$each'])
        )

        adapter.calculate_spent = MagicMock(return_value={'$all': 205})
        self.assertEqual(
            f'SPENT STATISTICS:\nperiod: 2022-12 to 2023-02\n$all: 205 {chr(8364)}\n',
            command.execute(adapter, ['2022-12', '2023-02', '$all'])
        )

        adapter.calculate_spent = MagicMock(return_value={'HOME': 45, 'basket': 10, 'plates': 35})
        self.assertEqual(
            f'SPENT STATISTICS:\nperiod: 2022-12 to 2022-12\nHOME: 45 {chr(8364)}\nbasket: 10 {chr(8364)}\nplates: 35 {chr(8364)}\n',
            command.execute(adapter, ['2022-12', 'home'])
        )

        adapter.calculate_spent = MagicMock(return_value={})
        self.assertRaisesRegex(
            NoPurchacesThisParametersException,
            'No purchases with these parameters.',
            command.execute,
            adapter,
            ['2022-12', '2023-02', 'polar_bear']
        )

        adapter.calculate_spent = MagicMock(return_value=None)
        self.assertRaisesRegex(
            FailedAccessDatabaseException,
            'No access to database. Failed to calculate spent!',
            command.execute,
            adapter,
            ['2022-12', '2023-02', '$each']
        )


if __name__ == '__main__':
    unittest.main()
