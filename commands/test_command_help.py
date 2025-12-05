import pytest
from commands.command_help import *


def test_validate_help_parameters():
    assert validate_help_parameters([])
    assert validate_help_parameters(["buy"])
    assert validate_help_parameters(["info"]) is False
    assert validate_help_parameters(["buy", "del"]) is False


@pytest.mark.unit_test
def test_command_execute():
    command = HelpCommandExecutor()
    result = command.execute(None, [])
    assert result["message"].startswith("Ollaidh BUDget BUDdy - track your budget")

    result = command.execute(None, ["buy"])
    assert result["message"].startswith('"!buy"')
    result = command.execute(None, ["spent"])
    assert result["message"].startswith('"!spent"')
    result = command.execute(None, ["del"])
    assert result["message"].startswith('"!del"')

    with pytest.raises(InvalidParametersException):
        command.execute(None, ["buy", "spent"])

    with pytest.raises(InvalidParametersException):
        command.execute(None, ["help"])
