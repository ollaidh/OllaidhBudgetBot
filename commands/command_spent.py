import datetime
from datetime import datetime
from typing import Optional
from commands.exceptions import *


def get_date(line: str) -> Optional[str]:
    if line == "today":
        return str(datetime.today().date())[:-3]
    try:
        return str(datetime.strptime(line, "%Y-%m").date())[:-3]
    except ValueError:
        return None


def validate_spent_param_len0(parameters: list[str], spent_parameters: dict) -> Optional[dict]:
    spent_parameters["start_date"] = get_date("today")
    spent_parameters["end_date"] = spent_parameters["start_date"]
    spent_parameters["category"] = "$each"
    return spent_parameters


def validate_spent_param_len1(parameters: list[str], spent_parameters: dict) -> Optional[dict]:
    if get_date(parameters[0]):
        spent_parameters["start_date"] = get_date(parameters[0])
        spent_parameters["end_date"] = spent_parameters["start_date"]
        spent_parameters["category"] = "$each"
    else:
        spent_parameters["start_date"] = get_date("today")
        spent_parameters["end_date"] = spent_parameters["start_date"]
        spent_parameters["category"] = parameters[0]
    return spent_parameters


def validate_spent_param_len2(parameters: list[str], spent_parameters: dict) -> Optional[dict]:
    if get_date(parameters[0]) and get_date(parameters[1]) and (get_date(parameters[0]) <= get_date(parameters[1])):
        spent_parameters["start_date"] = get_date(parameters[0])
        spent_parameters["end_date"] = get_date(parameters[1])
        spent_parameters["category"] = "$each"
    else:
        if get_date(parameters[0]):
            spent_parameters["start_date"] = get_date(parameters[0])
            spent_parameters["end_date"] = spent_parameters["start_date"]
            spent_parameters["category"] = parameters[1]
        else:
            return None
    return spent_parameters


def validate_spent_param_len3(parameters: list[str], spent_parameters: dict) -> Optional[dict]:
    if get_date(parameters[0]) and get_date(parameters[1]) and (get_date(parameters[0]) <= get_date(parameters[1])):
        spent_parameters["start_date"] = get_date(parameters[0])
        spent_parameters["end_date"] = get_date(parameters[1])
        spent_parameters["category"] = parameters[2]
        return spent_parameters
    return None


class SpentCommandExecutor:
    def __init__(self):
        self.validators = {
            0: validate_spent_param_len0,
            1: validate_spent_param_len1,
            2: validate_spent_param_len2,
            3: validate_spent_param_len3,
        }

    def validate(self, parameters: list[str]) -> Optional[dict]:
        spent_parameters = {"start_date": None, "end_date": None, "category": None}
        if not len(parameters) in self.validators:
            return None
        return self.validators[len(parameters)](parameters, spent_parameters)

    def execute(self, database_adapter, user_input: list[str]) -> dict:
        parameters = self.validate(user_input)
        if parameters:
            spent = database_adapter.calculate_spent(
                parameters["start_date"], parameters["end_date"], parameters["category"]
            )
            start = parameters["start_date"]
            end = parameters["end_date"]
            if spent:
                summary = ""
                for key, value in spent.items():
                    summary += f"{key}: {format(value, '.1f').rstrip('0').rstrip('.')} {chr(8364)}\n"
                return {"message": f"SPENT STATISTICS:\nperiod: {start} to {end}\n{summary}"}
            elif spent == {}:
                raise NoPurchacesThisParametersException
            raise FailedAccessDatabaseException("calculate spent")
        raise InvalidParametersException
