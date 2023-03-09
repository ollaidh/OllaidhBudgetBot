class BotException(Exception):
    pass


class FailedAccessDatabaseException(BotException):
    def __init__(self, action: str):
        self.action = action

    def __str__(self):
        return f'No access to database. Failed to {self.action}!'


class NoPurchacesThisParametersException(BotException):
    def __str__(self):
        return f'No purchases with these parameters.'


class InvalidCommandException(BotException):
    def __init__(self, command: str, accepted_commands: list[str]):
        self.command = command
        self.accepted_commands = accepted_commands

    def __str__(self):
        return f'Invalid command "{self.command}"! Valid commands are: {self.accepted_commands}.'


class InvalidParametersException(BotException):
    def __str__(self):
        return 'Invalid parameters!'


class NegativePriceException(InvalidParametersException):
    def __str__(self):
        return 'Invalid price: negative!'


class NotNumberPriceException(InvalidParametersException):
    def __str__(self):
        return 'Invalid price: not a number!'


class InvalidNumberParametersException(InvalidParametersException):
    def __str__(self):
        return 'Invalid number of parameters!'

