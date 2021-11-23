from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/call_same_method.lox
TEST_SRC = dedent(
    """\
    class Base {
      foo() {
        print "Base.foo()";
      }
    }

    class Derived < Base {
      foo() {
        print "Derived.foo()";
        super.foo();
      }
    }

    Derived().foo();
    // expect: Derived.foo()
    // expect: Base.foo()
    """
)

EXPECTED_STDOUTS = ["Derived.foo()", "Base.foo()"]


def test_call_same_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
