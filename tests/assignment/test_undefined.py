from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/undefined.lox
TEST_SRC = dedent(
    """\
    unknown = "what"; // expect runtime error: Undefined variable 'unknown'.
    """
)

EXPECTED_STDOUTS = ["1:1: LoxRuntimeError: Undefined variable 'unknown'."]


def test_to_this(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
