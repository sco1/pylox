from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/open_closure_in_function.lox
TEST_SRC = dedent(
    """\
    {
      var local = "local";
      fun f() {
        print local; // expect: local
      }
      f();
    }
    """
)

EXPECTED_STDOUTS = ["local"]


def test_open_closure_in_function(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
