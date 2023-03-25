import unittest
from commands.command_del import *
from unittest.mock import MagicMock


class TestDel(unittest.TestCase):
    def test_command_execute(self):
        command = DelCommandExecutor()

        class TestAdapter:
            pass

        adapter = TestAdapter()
        adapter.delete_purchase = MagicMock(return_value=True)
        self.assertEqual(
            {'message': 'DELETED: Last purchase'},
            command.execute(adapter, [])
        )

        adapter.delete_purchase = MagicMock(return_value=False)
        self.assertEqual(
            {'message': 'FAILED to delete last purchase from database'},
            command.execute(adapter, [])
        )

        self.assertRaises(InvalidParametersException, command.execute, adapter, ['purchase'])


if __name__ == '__main__':
    unittest.main()
