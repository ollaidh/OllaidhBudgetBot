import pytest
from commands.command_spent import *
from unittest.mock import MagicMock


@pytest.mark.unit_test
def test_get_date():
    assert get_date("today") == str(datetime.today().date())[:-3]
    assert get_date("2022-12") == "2022-12"
    assert get_date("january") is None


@pytest.mark.unit_test
def test_validate_spent_parameters():
    executor = SpentCommandExecutor()
    assert executor.validate(["2022-12", "2023-01", "takeaway"]) == {
        "start_date": "2022-12",
        "end_date": "2023-01",
        "category": "takeaway",
    }
    assert executor.validate(["2022-12", "2023-01"]) == {
        "start_date": "2022-12",
        "end_date": "2023-01",
        "category": "$each",
    }
    assert executor.validate(["2022-12", "takeaway"]) == {
        "start_date": "2022-12",
        "end_date": "2022-12",
        "category": "takeaway",
    }

    assert executor.validate(["takeaway"]) == {
        "start_date": str(datetime.today().date())[:-3],
        "end_date": str(datetime.today().date())[:-3],
        "category": "takeaway",
    }

    assert {"start_date": "2022-12", "end_date": "2022-12", "category": "$each"}, executor.validate(["2022-12"])

    assert executor.validate([]) == {
        "start_date": (str(datetime.today().date()))[:-3],
        "end_date": (str(datetime.today().date()))[:-3],
        "category": "$each",
    }

    assert executor.validate(["2022-12", "2023-01", "takeaway", "coffee"]) is None
    assert executor.validate(["takeaway", "2023-01", "2022-12"]) is None
    assert executor.validate(["takeaway", "2023-01"]) is None
    assert executor.validate(["2023-01", "2022-12", "dog"]) is None


@pytest.mark.unit_test
def test_command_execute():
    command = SpentCommandExecutor()

    class TestAdapter:
        pass

    adapter = TestAdapter()
    adapter.calculate_spent = MagicMock(return_value={"meat": 129.111111111, "takeaway": 76.2})

    assert command.execute(adapter, ["2022-12", "2023-02", "$each"]) == {
        "message": f"SPENT STATISTICS:\nperiod: 2022-12 to 2023-02\nmeat: 129.1 {chr(8364)}\ntakeaway: 76.2 {chr(8364)}\n"
    }

    adapter.calculate_spent = MagicMock(return_value={"$all": 205})
    assert command.execute(adapter, ["2022-12", "2023-02", "$all"]) == {
        "message": f"SPENT STATISTICS:\nperiod: 2022-12 to 2023-02\n$all: 205 {chr(8364)}\n"
    }

    adapter.calculate_spent = MagicMock(return_value={"HOME": 45, "basket": 10, "plates": 35})

    assert command.execute(adapter, ["2022-12", "home"]) == {
        "message": f"SPENT STATISTICS:\nperiod: 2022-12 to 2022-12\nHOME: 45 {chr(8364)}\nbasket: 10 {chr(8364)}\nplates: 35 {chr(8364)}\n"
    }

    adapter.calculate_spent = MagicMock(return_value={})

    with pytest.raises(NoPurchacesThisParametersException) as ex:
        command.execute(adapter, ["2022-12", "2023-02", "polar_bear"])
        assert str(ex.exception) == "No purchases with these parameters."

    adapter.calculate_spent = MagicMock(return_value=None)

    with pytest.raises(FailedAccessDatabaseException) as ex:
        command.execute(adapter, ["2022-12", "2023-02", "$each"])
        assert str(ex.exception) == "No access to database. Failed to calculate spent!"
