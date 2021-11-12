from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/negate_nonnum.lox
TEST_SRC = dedent(
    """\
    -"s"; // expect runtime error: Operand must be a number.
    """
)

EXPECTED_STDOUTS = ["1:1: LoxRuntimeError: Operands must be numbers."]


def test_negate_nonnum(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
