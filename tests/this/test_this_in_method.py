from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/this/this_in_method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      bar() { return this; }
      baz() { return "baz"; }
    }

    print Foo().bar().baz(); // expect: baz
    """
)

EXPECTED_STDOUTS = ["baz"]


def test_this_in_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
