from commands.exceptions import *
from commands.command_executor import CommandExecutor


class GetMonthSpendLimitCommandExecutor(CommandExecutor):
    def execute(self, database_adapter, user_input: list[str]) -> dict[str, str]:
        # month_spend_limit = self.validate(user_input)
        # comment = self.jibjab.month_limit_kind_warning(month_spend_limit) if month_spend_limit < 1500 else None
        limits = database_adapter.get_month_limit(user_input[0])
        if limits:
            return {"message": f"Current month limit: {limits[-1]} EUR\n Limit history: {limits}"}
        raise FailedAccessDatabaseException("set month spend limit")
