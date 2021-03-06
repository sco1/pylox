from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/set_evaluation_order.lox
TEST_SRC = dedent(
    """\
    undefined1.bar // expect runtime error: Undefined variable 'undefined1'.
      = undefined2;
    """
)

EXPECTED_STDOUTS = ["1:1: LoxRuntimeError: Undefined variable 'undefined1'."]


def test_set_evaluation_order(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
