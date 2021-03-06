from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/this/nested_class.lox
TEST_SRC = dedent(
    """\
    class Outer {
      method() {
        print this; // expect: Outer instance

        fun f() {
          print this; // expect: Outer instance

          class Inner {
            method() {
              print this; // expect: Inner instance
            }
          }

          Inner().method();
        }
        f();
      }
    }

    Outer().method();
    """
)

EXPECTED_STDOUTS = ["<inst Outer>", "<inst Outer>", "<inst Inner>"]


def test_nested_class(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
