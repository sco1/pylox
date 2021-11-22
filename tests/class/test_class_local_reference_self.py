from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/class/local_reference_self.lox
TEST_SRC = dedent(
    """\
    {
      class Foo {
        returnSelf() {
          return Foo;
        }
      }

      print Foo().returnSelf(); // expect: <cls Foo>
    }
    """
)

EXPECTED_STDOUTS = ["<cls Foo>"]


def test_local_reference_self(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
