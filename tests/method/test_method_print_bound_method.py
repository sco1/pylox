from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/method/print_bound_method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      method() { }
    }
    var foo = Foo();
    print foo.method; // expect: <fn method>
    """
)

EXPECTED_STDOUTS = ["<fn method>"]


def test_print_bound_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
