from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/duplicate_local.lox
TEST_SRC = dedent(
    """\
    {
      var a = "value";
      var a = "other"; // Error at 'a': Already a variable with this name in this scope.
    }
    """
)

EXPECTED_STDOUTS = ["3:7: LoxRuntimeError: Cannot redefine 'a' in a non-global scope."]


def test_duplicate_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
