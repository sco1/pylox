from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/less_or_equal_nonnum_num.lox
TEST_SRC = dedent(
    """\
    "1" <= 1; // expect runtime error: Operands must be numbers.
    """
)

EXPECTED_STDOUTS = ["1:5: LoxRuntimeError: Operands must be numbers."]


def test_less_or_equal_nonnum_num(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
