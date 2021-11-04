from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/shadow_and_local.lox
TEST_SRC = dedent(
    """\
    {
      var a = "outer";
      {
        print a; // expect: outer
        var a = "inner";
        print a; // expect: inner
      }
    }
    """
)

EXPECTED_STDOUTS = ["outer", "inner"]


def test_shadow_and_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
