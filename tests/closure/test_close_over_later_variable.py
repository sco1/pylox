from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/close_over_later_variable.lox
TEST_SRC = dedent(
    """\
    // This is a regression test. There was a bug where if an upvalue for an
    // earlier local (here "a") was captured *after* a later one ("b"), then it
    // would crash because it walked to the end of the upvalue list (correct), but
    // then didn't handle not finding the variable.

    fun f() {
      var a = "a";
      var b = "b";
      fun g() {
        print b; // expect: b
        print a; // expect: a
      }
      g();
    }
    f();
    """
)

EXPECTED_STDOUTS = ["b", "a"]


def test_close_over_later_variable(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
