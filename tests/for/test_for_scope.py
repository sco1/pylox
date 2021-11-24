from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/scope.lox
TEST_SRC = dedent(
    """\
    {
      var i = "before";

      // New variable is in inner scope.
      for (var i = 0; i < 1; i = i + 1) {
        print i; // expect: 0

        // Loop body is in second inner scope.
        var i = -1;
        print i; // expect: -1
      }
    }

    {
      // New variable shadows outer variable.
      for (var i = 0; i > 0; i = i + 1) {}

      // Goes out of scope after loop.
      var i = "after";
      print i; // expect: after

      // Can reuse an existing variable.
      for (i = 0; i < 1; i = i + 1) {
        print i; // expect: 0
      }
    }
    """
)

EXPECTED_STDOUTS = ["0", "-1", "after", "0"]


def test_scope(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
