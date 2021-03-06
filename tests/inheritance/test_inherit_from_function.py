from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/inherit_from_function.lox
TEST_SRC = dedent(
    """\
    fun foo() {}

    class Subclass < foo {} // expect runtime error: Superclass must be a class.
    """
)

EXPECTED_STDOUTS = ["3:18: LoxRuntimeError: Superclass must be a class."]


def test_inherit_from_function(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
