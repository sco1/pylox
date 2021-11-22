from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/get_on_function.lox
TEST_SRC = dedent(
    """\
    fun foo() {}

    foo.bar; // expect runtime error: Only instances have properties.
    """
)

EXPECTED_STDOUTS = ["3:5: LoxRuntimeError: Only instances have properties."]


def test_get_on_function(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
