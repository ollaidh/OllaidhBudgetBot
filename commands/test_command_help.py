import unittest
from commands.command_help import *


class TestHelp(unittest.TestCase):
    def test_validate_help_parameters(self):
        self.assertTrue(validate_help_parameters([]))
        self.assertTrue(validate_help_parameters(['buy']))
        self.assertFalse(validate_help_parameters(['info']))
        self.assertFalse(validate_help_parameters(['buy', 'del']))

    def test_command_execute(self):
        command = HelpCommandExecutor()
        result = command.execute(None, [])
        self.assertTrue(result.startswith('Ollaidh BUDget BUDdy - track your budget'))

        result = command.execute(None, ['buy'])
        self.assertTrue(result.startswith('"!buy"'))
        result = command.execute(None, ['spent'])
        self.assertTrue(result.startswith('"!spent"'))
        result = command.execute(None, ['del'])
        self.assertTrue(result.startswith('"!del"'))

        self.assertRaises(InvalidParametersException, command.execute, None, ['buy', 'spent'])
        self.assertRaises(InvalidParametersException, command.execute, None, ['help'])


if __name__ == '__main__':
    unittest.main()
