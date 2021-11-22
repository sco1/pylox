from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/extra_arguments.lox
TEST_SRC = dedent(
    """\
    class Base {
      foo(a, b) {
        print "Base.foo(" + a + ", " + b + ")";
      }
    }

    class Derived < Base {
      foo() {
        print "Derived.foo()"; // expect: Derived.foo()
        super.foo("a", "b", "c", "d"); // expect runtime error: Expected 2 arguments but got 4.
      }
    }

    Derived().foo();
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_extra_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
