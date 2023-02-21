class BotException(Exception):
    pass


class InvalidCommandException(BotException):
    def __init__(self, command: str, accepted_commands: list[str]):
        self.command = command
        self.accepted_commands = accepted_commands

    def __str__(self):
        return f'Invalid command "{self.command}"! Valid commands are: {self.accepted_commands}.'


class InvalidParametersException(BotException):
    def __str__(self):
        return 'Invalid parameters were passed!'

