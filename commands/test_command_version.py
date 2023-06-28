import unittest
from unittest.mock import patch
from commands.command_version import *


class TestVersion(unittest.TestCase):
    @patch('commands.command_version.get_date_today')
    def test_command_version(self, date_mocked):
        date_mocked.return_value = "2222.22.22"
        command = VersionCommandExecutor()
        result = command.execute(None, [])
        self.assertEqual({'message': "Bot version: 2222.22.22"}, result)
