from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/inherit_from_number.lox
TEST_SRC = dedent(
    """\
    var Number = 123;
    class Foo < Number {} // expect runtime error: Superclass must be a class.
    """
)

EXPECTED_STDOUTS = ["2:13: LoxRuntimeError: Superclass must be a class."]


def test_inherit_from_number(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
