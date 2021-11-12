from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/add_num_nil.lox
TEST_SRC = dedent(
    """\
    1 + nil; // expect runtime error: Operands must be two numbers or two strings.
    """
)

EXPECTED_STDOUTS = ["1:3: LoxRuntimeError: Operands must either be both numbers or both strings."]


def test_add_num_nil(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
