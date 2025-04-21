from commands.exceptions import *


class DelCommandExecutor:
    def validate(self, parameters: list[str]) -> bool:
        if not parameters:
            return True
        return False

    def execute(self, database_adapter, parameters: list[str]) -> dict:
        if self.validate(parameters):
            deleted = database_adapter.delete_purchase()
            if deleted:
                return {"message": "DELETED: Last purchase"}
            return {"message": "FAILED to delete last purchase from database"}
        raise InvalidParametersException
