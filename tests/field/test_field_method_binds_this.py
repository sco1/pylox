from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/method_binds_this.lox
TEST_SRC = dedent(
    """\
    class Foo {
      sayName(a) {
        print this.name;
        print a;
      }
    }

    var foo1 = Foo();
    foo1.name = "foo1";

    var foo2 = Foo();
    foo2.name = "foo2";

    // Store the method reference on another object.
    foo2.fn = foo1.sayName;
    // Still retains original receiver.
    foo2.fn(1);
    // expect: foo1
    // expect: 1
    """
)

EXPECTED_STDOUTS = ["foo1", "1"]


def test_method_binds_this(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
