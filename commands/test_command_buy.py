import pytest
from unittest.mock import MagicMock
from commands.command_buy import *
from db_adapters.adapter import PurchaseInfo


@pytest.mark.unit_test
def test_get_category():
    assert get_category("water") == "utilities"
    assert get_category("candibober") == "uncategorized"


@pytest.mark.unit_test
def test_validate_buy_parameters():
    buy = BuyCommandExecutor()
    assert buy.validate(["coffee", "2.5", "takeout"]) == PurchaseInfo("coffee", 2.5, "takeout")

    with pytest.raises(InvalidNumberParametersException) as ex:
        buy.validate(["coffee", 0, 12, "takeout"])
        assert str(ex.exception) == "Invalid number of parameters!"

    with pytest.raises(NegativePriceException) as ex:
        buy.validate(["coffee", -5, "takeout"])
        assert str(ex.exception) == "Invalid price: negative!"

    with pytest.raises(NotNumberPriceException) as ex:
        buy.validate(["coffee", "one euro", "takeout"])
        assert str(ex.exception) == "Invalid price: not a number!"


@pytest.mark.unit_test
def test_command_execute():
    command = BuyCommandExecutor()

    class TestAdapter:
        pass

    adapter = TestAdapter()
    adapter.add_purchase = MagicMock(return_value=True)
    result = command.execute(adapter, ["coffee", 2.5, "takeout"])

    assert result["message"].startswith("ADDED PURCHASE: coffee 2.5 takeout")

    adapter.add_purchase.assert_called_once_with(PurchaseInfo("coffee", 2.5, "takeout"))
    adapter.add_purchase.reset_mock()

    adapter.add_purchase = MagicMock(return_value=False)

    with pytest.raises(FailedAccessDatabaseException) as ex:
        command.execute(adapter, ["chicken", 8, "meat"])
        assert str(ex.exception) == "No access to database. Failed to add purchase!"
