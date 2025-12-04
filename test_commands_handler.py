import pytest
from commands_handler import *
from commands.exceptions import *
from unittest.mock import MagicMock
from db_adapters.adapter import PurchaseInfo


@pytest.mark.unit_test
def test_handle_message():
    class TestAdapter:
        def add_purchase(self, purchase: PurchaseInfo) -> bool:
            return True

        def delete_purchase(self) -> bool:
            return True

        def calculate_spent(self, start_date: str, end_date: str, category: str) -> Optional[dict]:
            return {}

    class TestJibberJabber:
        pass

    adapter = TestAdapter()
    handler = CommandsHandler(adapter)

    adapter.add_purchase = MagicMock(return_value=True)

    # *.startswith() is used to ignore random jibber jabber comments after th block ADDED PURCHASE
    assert handler.handle_message("!buy\ncoffee\n3.5")["message"].startswith("ADDED PURCHASE: coffee 3.5") is True
    assert handler.handle_message("!buy\ncoffee 3.5")["message"].startswith("ADDED PURCHASE: coffee 3.5") is True
    assert handler.handle_message("!buy coffee 3.5")["message"].startswith("ADDED PURCHASE: coffee 3.5") is True

    with pytest.raises(InvalidCommandException) as ex:
        handler.handle_message("!purchased\ncoffee 3.5")

        assert str(ex.exception).startswith("Invalid command") is True
        assert ex.exception.command == "!purchased"
        assert ("!help" in ex.exception.accepted_commands) is True
        assert ("!buy" in ex.exception.accepted_commands) is True
        assert ("!spent" in ex.exception.accepted_commands) is True
        assert ("!del" in ex.exception.accepted_commands) is True
        assert ("!version" in ex.exception.accepted_commands) is True

    with pytest.raises(InvalidParametersException):
        handler.handle_message("!spent\ncoffee 2012-01-01")
