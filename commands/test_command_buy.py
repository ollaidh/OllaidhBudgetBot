import unittest
from unittest.mock import MagicMock
from commands.command_buy import *
from db_adapters.adapter import PurchaseInfo


class TestBuy(unittest.TestCase):
    def test_get_category(self):
        self.assertEqual(get_category('water'), 'utilities')
        self.assertEqual(get_category('candibober'), 'uncategorized')

    def test_validate_buy_parameters(self):
        buy = BuyCommandExecutor()
        self.assertEqual(buy.validate(['coffee', '2.5', 'takeout']), PurchaseInfo('coffee', 2.5, 'takeout'))

        self.assertRaisesRegex(
            InvalidNumberParametersException,
            'Invalid number of parameters!',
            buy.validate,
            ['coffee', 0, 12, 'takeout']
        )

        self.assertRaisesRegex(
            NegativePriceException,
            'Invalid price: negative!',
            buy.validate,
            ['coffee', -5, 'takeout']
        )

        self.assertRaisesRegex(
            NotNumberPriceException,
            'Invalid price: not a number!',
            buy.validate,
            ['coffee', 'O.O', 'takeout']
        )

    def test_command_execute(self):
        command = BuyCommandExecutor()

        class TestAdapter:
            pass

        adapter = TestAdapter()
        adapter.add_purchase = MagicMock(return_value=True)
        self.assertTrue(command.execute(adapter, ['coffee', '2.5', 'takeout']).
                        startswith('ADDED PURCHASE: coffee 2.5 takeout'))
        adapter.add_purchase.assert_called_once_with(PurchaseInfo('coffee', 2.5, 'takeout'))

        adapter.add_purchase.reset_mock()
        adapter.add_purchase = MagicMock(return_value=False)
        self.assertEqual(
            'FAILED TO ADD coffee 2.5 takeout TO DATABASE',
            command.execute(adapter, ['coffee', '2.5', 'takeout'])
        )
        adapter.add_purchase.assert_called_once_with(PurchaseInfo('coffee', 2.5, 'takeout'))


if __name__ == '__main__':
    unittest.main()
    