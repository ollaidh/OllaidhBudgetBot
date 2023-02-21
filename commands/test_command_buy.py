import unittest
from unittest.mock import MagicMock
from commands.command_buy import *


class TestBuy(unittest.TestCase):
    def test_get_category(self):
        self.assertEqual(get_category('water'), 'utilities')
        self.assertEqual(get_category('candibober'), 'uncategorized')

    def test_validate(self):
        validated, parameters = validate_buy_parameters(['coffee', '2.5', 'takeaway'])
        self.assertTrue(validated)
        self.assertEqual(parameters, ['coffee', '2.5', 'takeaway'])
        validated, parameters = validate_buy_parameters(['coffee', '2.5'])
        self.assertTrue(validated)
        self.assertEqual(parameters, ['coffee', '2.5', 'takeaway'])
        validated, parameters = validate_buy_parameters(['coffee', '2.'])
        self.assertTrue(validated)
        validated, parameters = validate_buy_parameters(['coffee', '.5'])
        self.assertTrue(validated)
        validated, parameters = validate_buy_parameters(['coffee', 'o.5'])
        self.assertFalse(validated)
        validated, parameters = validate_buy_parameters(['coffee', '-5'])
        self.assertFalse(validated)
        validated, parameters = validate_buy_parameters(['coffee', 'takeaway'])
        self.assertFalse(validated)
        validated, parameters = validate_buy_parameters([])
        self.assertFalse(validated)
        validated, parameters = validate_buy_parameters(['2'])
        self.assertFalse(validated)
        validated, parameters = validate_buy_parameters(['2', 'takeaway'])
        self.assertFalse(validated)

    def test_command_execute(self):
        command = BuyCommandExecutor()

        class TestAdapter:
            pass

        adapter = TestAdapter()
        adapter.add_purchase = MagicMock(return_value=True)
        self.assertEqual(
            'ADDED PURCHASE: coffee 2.5 takeout',
            command.execute(adapter, ['coffee', '2.5', 'takeout'])
        )
        adapter.add_purchase.assert_called_once_with('coffee', '2.5', 'takeout')

        adapter.add_purchase.reset_mock()
        adapter.add_purchase = MagicMock(return_value=False)
        self.assertEqual(
            'FAILED TO ADD coffee 2.5 takeout TO DATABASE',
            command.execute(adapter, ['coffee', '2.5', 'takeout'])
        )
        adapter.add_purchase.assert_called_once_with('coffee', '2.5', 'takeout')

        self.assertRaises(
            InvalidParametersException,
            command.execute,
            adapter,
            ['coffee', 'o.O', 'takeout']
        )


if __name__ == '__main__':
    unittest.main()
    