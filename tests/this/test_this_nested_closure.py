from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/this/nested_closure.lox
TEST_SRC = dedent(
    """\
    class Foo {
      getClosure() {
        fun f() {
          fun g() {
            fun h() {
              return this.toString();
            }
            return h;
          }
          return g;
        }
        return f;
      }

      toString() { return "Foo"; }
    }

    var closure = Foo().getClosure();
    print closure()()(); // expect: Foo
    """
)

EXPECTED_STDOUTS = ["Foo"]


def test_nested_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
