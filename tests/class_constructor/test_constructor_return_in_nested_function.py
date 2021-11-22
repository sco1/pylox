from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/return_in_nested_function.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init() {
        fun init() {
          return "bar";
        }
        print init(); // expect: bar
      }
    }

    print Foo(); // expect: Foo instance
    """
)

EXPECTED_STDOUTS = ["bar", "<inst Foo>"]


def test_return_in_nested_function(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
