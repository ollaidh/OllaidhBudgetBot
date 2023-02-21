from commands.exceptions import *


def get_category(item: str) -> str:
    categories = {
        'meat': ('steak', 'pork', 'chicken', 'liver', 'bacon', 'meat'),
        'takeaway': ('coffee', 'pasrty', 'breakfast', 'lunch', 'dinner', 'takeaway'),
        'utilities': ('electricity', 'water', 'internet'),
        'sweets': ('cookies', 'chocolate', 'sweets'),
        'vegetables': ('potatoes', 'green', 'avocado', 'vegetables')
    }
    for category, items in categories.items():
        if item in items:
            return category
    return 'uncategorized'


def validate_buy_parameters(parameters: list[str]) -> (bool, list[str]):
    if len(parameters) < 2 or len(parameters) > 3:
        return False, []
    try:
        price = float(parameters[1])
        if price <= 0:
            return False, []
        if len(parameters) == 3:
            return True, [parameters[0], parameters[1], parameters[2]]
        category = get_category(parameters[0])
        return True, [parameters[0], parameters[1], category]
    except ValueError:
        return False, []


class BuyCommandExecutor:
    def execute(self, database_adapter, user_input: list[str]) -> str:
        validated, parameters = validate_buy_parameters(user_input)
        if validated:
            buy = database_adapter.add_purchase(parameters[0], parameters[1], parameters[2])
            purchase = ' '.join(user_input)
            if buy:
                return f'ADDED PURCHASE: {purchase}'
            return f'FAILED TO ADD {purchase} TO DATABASE'
        raise InvalidParametersException
