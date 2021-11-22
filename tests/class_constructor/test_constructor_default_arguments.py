from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/default_arguments.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    var foo = Foo(1, 2, 3); // expect runtime error: Expected 0 arguments but got 3.
    """
)

EXPECTED_STDOUTS = ["3:22: LoxRuntimeError: Expected 0 arguments but got 3."]


def test_default_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
