from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/assign_to_closure.lox
TEST_SRC = dedent(
    """\
    var f;
    var g;

    {
      var local = "local";
      fun f_() {
        print local;
        local = "after f";
        print local;
      }
      f = f_;

      fun g_() {
        print local;
        local = "after g";
        print local;
      }
      g = g_;
    }

    f();
    // expect: local
    // expect: after f

    g();
    // expect: after f
    // expect: after g
    """
)

EXPECTED_STDOUTS = ["local", "after f", "after f", "after g"]


def test_assign_to_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
