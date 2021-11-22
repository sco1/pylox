from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/call_nonfunction_field.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    var foo = Foo();
    foo.bar = "not fn";

    foo.bar(); // expect runtime error: Can only call functions and classes.
    """
)

EXPECTED_STDOUTS = ["6:9: LoxRuntimeError: Can only call functions and classes."]


def test_call_nonfunction_field(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
