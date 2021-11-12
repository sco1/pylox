from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/reference_closure_multiple_times.lox
TEST_SRC = dedent(
    """\
    var f;

    {
      var a = "a";
      fun f_() {
        print a;
        print a;
      }
      f = f_;
    }

    f();
    // expect: a
    // expect: a
    """
)

EXPECTED_STDOUTS = ["a", "a"]


def test_reference_closure_multiple_times(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
