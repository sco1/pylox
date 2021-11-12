from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/reuse_closure_slot.lox
TEST_SRC = dedent(
    """\
    {
      var f;

      {
        var a = "a";
        fun f_() { print a; }
        f = f_;
      }

      {
        // Since a is out of scope, the local slot will be reused by b. Make sure
        // that f still closes over a.
        var b = "b";
        f(); // expect: a
      }
    }
    """
)

EXPECTED_STDOUTS = ["a"]


def test_reuse_closure_slot(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
