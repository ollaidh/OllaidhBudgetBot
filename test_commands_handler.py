import unittest
from commands_handler import *
from commands.exceptions import *
from unittest.mock import MagicMock
from db_adapters.adapter import PurchaseInfo


class TestCommandsHandler(unittest.TestCase):
    def test_handle_message(self):
        class TestAdapter:
            def add_purchase(self, purchase: PurchaseInfo) -> bool:
                return True

            def delete_purchase(self) -> bool:
                return True

            def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
                return {}

        class TestJibberJabber:
            pass

        adapter = TestAdapter()
        handler = CommandsHandler(adapter)

        adapter.add_purchase = MagicMock(return_value=True)

        # *.startswith() is used to ignore random jibber jabber comments after th block ADDED PURCHASE
        self.assertTrue(handler.handle_message('!buy\ncoffee\n3.5')['message'].startswith('ADDED PURCHASE: coffee 3.5'))
        self.assertTrue(handler.handle_message('!buy\ncoffee 3.5')['message'].startswith('ADDED PURCHASE: coffee 3.5'))
        self.assertTrue(handler.handle_message('!buy coffee 3.5')['message'].startswith('ADDED PURCHASE: coffee 3.5'))

        with self.assertRaises(InvalidCommandException) as ex:
            handler.handle_message('!purchased\ncoffee 3.5')
        self.assertTrue(str(ex.exception).startswith("Invalid command"))
        self.assertEqual(ex.exception.command, '!purchased')
        self.assertTrue('!help' in ex.exception.accepted_commands)
        self.assertTrue('!buy' in ex.exception.accepted_commands)
        self.assertTrue('!spent' in ex.exception.accepted_commands)
        self.assertTrue('!del' in ex.exception.accepted_commands)
        self.assertTrue('!version' in ex.exception.accepted_commands)

        self.assertRaises(InvalidParametersException, handler.handle_message, '!spent\ncoffee 2012-01-01')


if __name__ == '__main__':
    unittest.main()
