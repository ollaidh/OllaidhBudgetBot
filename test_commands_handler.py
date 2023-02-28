import unittest
from commands_handler import *
from commands.exceptions import *
from unittest.mock import MagicMock


class TestCommandsHandler(unittest.TestCase):
    def test_handle_message(self):
        class TestAdapter:
            pass

        adapter = TestAdapter()
        handler = CommandsHandler(adapter)

        adapter.add_purchase = MagicMock(return_value=True)
        self.assertEqual(handler.handle_message('!buy\ncoffee\n3.5'), 'ADDED PURCHASE: coffee 3.5')
        self.assertEqual(handler.handle_message('!buy\ncoffee 3.5'), 'ADDED PURCHASE: coffee 3.5')
        self.assertEqual(handler.handle_message('!buy coffee 3.5'), 'ADDED PURCHASE: coffee 3.5')

        with self.assertRaises(InvalidCommandException) as ex:
            handler.handle_message('!purchased\ncoffee 3.5')
        self.assertTrue(str(ex.exception).startswith("Invalid command"))
        self.assertEqual(ex.exception.command, '!purchased')
        self.assertTrue('!help' in ex.exception.accepted_commands)
        self.assertTrue('!buy' in ex.exception.accepted_commands)
        self.assertTrue('!spent' in ex.exception.accepted_commands)
        self.assertTrue('!del' in ex.exception.accepted_commands)

        self.assertRaises(InvalidParametersException, handler.handle_message, '!spent\ncoffee 2012-01-01')


if __name__ == '__main__':
    unittest.main()
