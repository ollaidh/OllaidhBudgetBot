import commands
from typing import Optional
from db_adapters.adapter import Adapter


class CommandsHandler:
    def __init__(self, database_adapter: Adapter):
        self.executors = {
            '!help': commands.HelpCommandExecutor(),
            '!buy': commands.BuyCommandExecutor(),
            '!del': commands.DelCommandExecutor(),
            '!spent': commands.SpentCommandExecutor(),
            '!chart': commands.ChartCommandExecutor(),
            '!version': commands.VersionCommandExecutor()
        }
        self.database_adapter = database_adapter

    def handle_message(self, msg: str) -> Optional[dict]:
        if msg.startswith('!'):
            msg = msg.split()
            command = msg[0]

            if command not in self.executors:
                raise commands.InvalidCommandException(command, list(self.executors.keys()))
            parameters = msg[1:]
            return self.executors[command].execute(self.database_adapter, parameters)
        return None



