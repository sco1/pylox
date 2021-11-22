from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/set_on_bool.lox
TEST_SRC = dedent(
    """\
    true.foo = "value"; // expect runtime error: Only instances have fields.
    """
)

EXPECTED_STDOUTS = ["1:6: LoxRuntimeError: Only instances have fields."]


def test_set_on_bool(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
