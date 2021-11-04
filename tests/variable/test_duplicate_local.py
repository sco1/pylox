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

EXPECTED_STDOUTS = ["Error at 'a': Already a variable with this name in this scope."]


@pytest.mark.xfail(reason="Not implemented")
def test_duplicate_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
