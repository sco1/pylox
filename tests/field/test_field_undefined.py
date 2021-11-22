from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/undefined.lox
TEST_SRC = dedent(
    """\
    class Foo {}
    var foo = Foo();

    foo.bar; // expect runtime error: Undefined property 'bar'.
    """
)

EXPECTED_STDOUTS = ["4:5: LoxRuntimeError: Undefined property 'bar'."]


def test_undefined(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
