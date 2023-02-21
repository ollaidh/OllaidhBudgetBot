import unittest
from commands_handler import *
from commands.exceptions import *
from firestore_adapter import FirestoreAdapter


class TestCommandsHandler(unittest.TestCase):
    def test_handle_message(self):
        adapter = FirestoreAdapter()
        handler = CommandsHandler(adapter)

        self.assertEqual(handler.handle_message('!buy\ncoffee\n3.5'), 'ADDED PURCHASE: coffee 3.5')

        with self.assertRaises(InvalidCommandException) as ex:
            handler.handle_message('!purchased\ncoffee\n3.5')
        self.assertTrue(str(ex.exception).startswith("Invalid command"))
        self.assertEqual(ex.exception.command, '!purchased')
        self.assertTrue('!help' in ex.exception.accepted_commands)
        self.assertTrue('!buy' in ex.exception.accepted_commands)
        self.assertTrue('!spent' in ex.exception.accepted_commands)
        self.assertTrue('!del' in ex.exception.accepted_commands)

        self.assertRaises(InvalidParametersException, handler.handle_message, '!spent\ncoffee\n2012-01-01')


if __name__ == '__main__':
    unittest.main()
