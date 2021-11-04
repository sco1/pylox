from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/shadow_local.lox
TEST_SRC = dedent(
    """\
    {
      var a = "local";
      {
        var a = "shadow";
        print a; // expect: shadow
      }
      print a; // expect: local
    }
    """
)

EXPECTED_STDOUTS = ["shadow", "local"]


def test_shadow_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
