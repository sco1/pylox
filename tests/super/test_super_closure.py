from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/closure.lox
TEST_SRC = dedent(
    """\
    class Base {
      toString() { return "Base"; }
    }

    class Derived < Base {
      getClosure() {
        fun closure() {
          return super.toString();
        }
        return closure;
      }

      toString() { return "Derived"; }
    }

    var closure = Derived().getClosure();
    print closure(); // expect: Base
    """
)

EXPECTED_STDOUTS = ["Base"]


def test_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
