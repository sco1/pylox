from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/assign_to_shadowed_later.lox
TEST_SRC = dedent(
    """\
    var a = "global";

    {
      fun assign() {
        a = "assigned";
      }

      var a = "inner";
      assign();
      print a; // expect: inner
    }

    print a; // expect: assigned
    """
)

EXPECTED_STDOUTS = ["inner", "assigned"]


def test_assign_to_shadowed_later(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
