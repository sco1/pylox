from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/call/bool.lox
TEST_SRC = dedent(
    """\
    true(); // expect runtime error: Can only call functions and classes.
    """
)

EXPECTED_STDOUTS = ["1:6: LoxRuntimeError: Can only call functions and classes."]


def test_bool(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
