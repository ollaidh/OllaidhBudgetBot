
class VersionCommandExecutor:
    def execute(self, database_adapter, parameters: list[str]) -> dict:
        version = '1.0.0'
        return {'message': f'Bot version: {version}'}
