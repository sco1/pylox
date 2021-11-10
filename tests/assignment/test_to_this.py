from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/to_this.lox
TEST_SRC = dedent(
    """\
    class Foo {
    Foo() {
        this = "value"; // Error at '=': Invalid assignment target.
    }
    }

    Foo();
    """
)

EXPECTED_STDOUTS = ["Error at '=': Invalid assignment target."]


@pytest.mark.xfail(reason="Classes not implemented.")
def test_to_this(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
