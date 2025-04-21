from commands.exceptions import *
from jibberjabber import JibberJabber


class SetMonthSpendLimitCommandExecutor:
    def __init__(self):
        self.jibjab = JibberJabber()

    def validate(self, user_input: list[str]) -> PurchaseInfo:
        try:
            month_spend_limit = int(user_input[0])
            if month_spend_limit < 1500:  # TODO remove hardcode, do better
                self.jibjab.month_limit_kind_warning(month_spend_limit)
        except ValueError:
            raise InvalidParametersException

    def execute(self, database_adapter, user_input: list[str]) -> dict:
        parameters = self.validate(user_input)
        buy = database_adapter.add_purchase(PurchaseInfo(parameters.name, parameters.price, parameters.category))
        purchase = f"{parameters.name} {parameters.price} {parameters.category}"
        comment = self.jibjab.toxic_response(parameters.name, parameters.category)
        if buy:
            return {"message": f"ADDED PURCHASE: {purchase}\n{comment}"}
        raise FailedAccessDatabaseException("add purchase")
