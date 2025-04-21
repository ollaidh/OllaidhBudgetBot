from commands.exceptions import *
from commands.command_executor import CommandExecutor
from jibberjabber import JibberJabber
from db_adapters.adapter import PurchaseInfo


def get_category(item: str) -> str:
    categories = {
        "meat": ("steak", "pork", "chicken", "liver", "bacon", "meat"),
        "takeaway": ("coffee", "pasrty", "breakfast", "lunch", "dinner", "takeaway"),
        "utilities": ("electricity", "water", "internet"),
        "sweets": ("cookies", "chocolate", "sweets"),
        "vegetables": ("potatoes", "green", "avocado", "vegetables"),
        "dairy": ("milk", "yogurt", "cheese", "dairy"),
    }
    for category, items in categories.items():
        if item in items:
            return category
    return "uncategorized"


class BuyCommandExecutor(CommandExecutor):
    def __init__(self):
        self.jibjab = JibberJabber()

    def validate(self, parameters: list[str]) -> PurchaseInfo:
        if len(parameters) < 2 or len(parameters) > 3:
            raise InvalidNumberParametersException
        try:
            price = float(parameters[1])
            if price <= 0:
                raise NegativePriceException
            if len(parameters) == 3:
                return PurchaseInfo(parameters[0], price, parameters[2])
            category = get_category(parameters[0])
            return PurchaseInfo(parameters[0], price, category)
        except ValueError:
            raise NotNumberPriceException

    def execute(self, database_adapter, user_input: list[str]) -> dict:
        parameters = self.validate(user_input)
        buy = database_adapter.add_purchase(PurchaseInfo(parameters.name, parameters.price, parameters.category))
        purchase = f"{parameters.name} {parameters.price} {parameters.category}"
        comment = self.jibjab.toxic_response(parameters.name, parameters.category)
        if buy:
            return {"message": f"ADDED PURCHASE: {purchase}\n{comment}"}
        raise FailedAccessDatabaseException("add purchase")
