from date_utils import get_date_today


class VersionCommandExecutor:
    def execute(self, database_adapter, parameters: list[str]) -> dict:
        version = get_date_today().replace("-", ".")
        return {'message': f'Bot version: {version}'}
