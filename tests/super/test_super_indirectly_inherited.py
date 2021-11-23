from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/indirectly_inherited.lox
TEST_SRC = dedent(
    """\
    class A {
      foo() {
        print "A.foo()";
      }
    }

    class B < A {}

    class C < B {
      foo() {
        print "C.foo()";
        super.foo();
      }
    }

    C().foo();
    // expect: C.foo()
    // expect: A.foo()
    """
)

EXPECTED_STDOUTS = ["C.foo()", "A.foo()"]


def test_indirectly_inherited(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
