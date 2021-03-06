from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/arguments.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init(a, b) {
        print "init"; // expect: init
        this.a = a;
        this.b = b;
      }
    }

    var foo = Foo(1, 2);
    print foo.a; // expect: 1
    print foo.b; // expect: 2
    """
)

EXPECTED_STDOUTS = ["init", "1", "2"]


def test_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
