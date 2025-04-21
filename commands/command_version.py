from commands.command_executor import CommandExecutor


class VersionCommandExecutor(CommandExecutor):
    def execute(self, database_adapter, parameters: list[str]) -> dict:
        version = "1.0.0"
        return {"message": f"Bot version: {version}"}
