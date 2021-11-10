from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/undefined_local.lox
TEST_SRC = dedent(
    """\
    {
      print notDefined;  // expect runtime error: Undefined variable 'notDefined'.
    }
    """
)

EXPECTED_STDOUTS = ["2:9: LoxRuntimeError: Undefined variable 'notDefined'."]


def test_undefined_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
