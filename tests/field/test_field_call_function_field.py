from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/call_function_field.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    fun bar(a, b) {
      print "bar";
      print a;
      print b;
    }

    var foo = Foo();
    foo.bar = bar;

    foo.bar(1, 2);
    // expect: bar
    // expect: 1
    // expect: 2
    """
)

EXPECTED_STDOUTS = ["bar", "1", "2"]


def test_call_function_field(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
