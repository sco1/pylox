from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/greater_num_nonnum.lox
TEST_SRC = dedent(
    """\
    1 > "1"; // expect runtime error: Operands must be numbers.
    """
)

EXPECTED_STDOUTS = ["1:3: LoxRuntimeError: Operands must be numbers."]


def test_greater_num_nonnum(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
