from commands.exceptions import *


def validate_help_parameters(parameters) -> bool:
    if not parameters:
        return True
    help_items = {'buy', 'del', 'spent'}
    if len(parameters) > 1:
        return False
    return parameters[0] in help_items


class HelpCommandExecutor:
    def execute(self, database_adapter, parameters: list[str]) -> dict:
        help_info = {
            None: 'Ollaidh BUDget BUDdy - track your budget.\nCommands: buy, del, spent\nTo get info on each command, '
                  'type "!help %command_name%"',
            'buy': '"!buy" command adds your purchase to database. Syntax: "!buy %item% %price_in_euro% %category% ('
                   'optional)".\nExample:\n!buy coffee 2.5 takeaway',
            'del': '"!del" command deletes your last purchase from database',
            'spent': '"!spent" command gets the spent amount of money for selected period and category. Syntax: "!spent '
                     '%startdate% %enddate% %category%".\nThe following combinations of arguments can be passed:\n'
                     '1. No argumemts - calculates spent amount for current month for all categories.\n'
                     '2. %startdate% %enddate% - calculates spent amount for selected period for all categories.\n'
                     'Example: !spent 2022-12 2023-01\n'
                     '3. %category% - calculates spent amount for all time for selected category\n'
                     'Example: !spent meat\n'
                     '4. %startdate% %enddate% %category% - calculates spent amount for selected period and category\n'
                     'Example: !spent 2022-12 2023-01 meat\n'
                     '5. %period% %category% - calculates spent amount for selected period (month or year) and category.\n'
                     '%period% format:\n"%Y-%m" - ex. "2022-12" or %Y - ex. "2022"\n'
                     'Example: !spent 2022-12 meat\n'
                     '6. %period% - calculates spent amount for selected period (month or year) for all categories.\n'
                     '%period% format:\n"%Y-%m" - ex. "2022-12" or %Y - ex. "2022"\n'
                     'Example:\n!spent 2022'
        }
        if not parameters:
            return {'message': help_info[None]}
        if validate_help_parameters(parameters):
            return {'message': help_info[parameters[0]]}
        raise InvalidParametersException
