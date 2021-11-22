from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/this/closure.lox
TEST_SRC = dedent(
    """\
    class Foo {
      getClosure() {
        fun closure() {
          return this.toString();
        }
        return closure;
      }

      toString() { return "Foo"; }
    }

    var closure = Foo().getClosure();
    print closure(); // expect: Foo
    """
)

EXPECTED_STDOUTS = ["Foo"]


def test_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
