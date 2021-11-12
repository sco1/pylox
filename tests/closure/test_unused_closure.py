from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/unused_closure.lox
TEST_SRC = dedent(
    """\
    // This is a regression test. There was a bug where the VM would try to close
    // an upvalue even if the upvalue was never created because the codepath for
    // the closure was not executed.

    {
      var a = "a";
      if (false) {
        fun foo() { a; }
      }
    }

    // If we get here, we didn't segfault when a went out of scope.
    print "ok"; // expect: ok
    """
)

EXPECTED_STDOUTS = ["ok"]


def test_unused_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
