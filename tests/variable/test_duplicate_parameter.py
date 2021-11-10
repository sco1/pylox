from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/duplicate_parameter.lox
TEST_SRC = dedent(
    """\
    fun foo(arg,
            arg) { // Error at 'arg': Already a variable with this name in this scope.
      "body";
    }
    """
)

EXPECTED_STDOUTS = ["Error at 'arg': Already a variable with this name in this scope."]


@pytest.mark.xfail(reason="Functions not implemented")
def test_duplicate_parameter(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
