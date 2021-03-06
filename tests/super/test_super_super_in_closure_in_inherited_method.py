from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/super_in_closure_in_inherited_method.lox
TEST_SRC = dedent(
    """\
    class A {
      say() {
        print "A";
      }
    }

    class B < A {
      getClosure() {
        fun closure() {
          super.say();
        }
        return closure;
      }

      say() {
        print "B";
      }
    }

    class C < B {
      say() {
        print "C";
      }
    }

    C().getClosure()(); // expect: A
    """
)

EXPECTED_STDOUTS = ["A"]


def test_super_in_closure_in_inherited_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
