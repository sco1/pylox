from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/bound_method.lox
TEST_SRC = dedent(
    """\
    class A {
      method(arg) {
        print "A.method(" + arg + ")";
      }
    }

    class B < A {
      getClosure() {
        return super.method;
      }

      method(arg) {
        print "B.method(" + arg + ")";
      }
    }


    var closure = B().getClosure();
    closure("arg"); // expect: A.method(arg)
    """
)

EXPECTED_STDOUTS = ["A.method(arg)"]


def test_bound_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
