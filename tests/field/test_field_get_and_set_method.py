from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/get_and_set_method.lox
TEST_SRC = dedent(
    """\
    // Bound methods have identity equality.
    class Foo {
      method(a) {
        print "method";
        print a;
      }
      other(a) {
        print "other";
        print a;
      }
    }

    var foo = Foo();
    var method = foo.method;

    // Setting a property shadows the instance method.
    foo.method = foo.other;
    foo.method(1);
    // expect: other
    // expect: 1

    // The old method handle still points to the original method.
    method(2);
    // expect: method
    // expect: 2
    """
)

EXPECTED_STDOUTS = ["other", "1", "method", "2"]


def test_get_and_set_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
