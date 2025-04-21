from commands.exceptions import *
from commands.command_executor import CommandExecutor
from jibberjabber import JibberJabber


class SetMonthSpendLimitCommandExecutor(CommandExecutor):
    def __init__(self):
        self.jibjab = JibberJabber()

    def validate(self, user_input: list[str]):
        try:
            month_spend_limit = int(user_input[0])
            if month_spend_limit <= 0:
                raise ValueError
            return month_spend_limit
        except ValueError:
            raise InvalidParametersException

    def execute(self, database_adapter, user_input: list[str]) -> dict[str, str]:
        month_spend_limit = self.validate(user_input)
        comment = self.jibjab.month_limit_kind_warning(month_spend_limit) if month_spend_limit < 1500 else None
        added_month_limit = database_adapter.set_month_limit(month_spend_limit)
        if added_month_limit:
            return {"message": f"MONTH SPENT LIMIT SET: {month_spend_limit} EUR\n{comment}"}
        raise FailedAccessDatabaseException("add purchase")
