from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/shadow_global.lox
TEST_SRC = dedent(
    """\
    var a = "global";
    {
      var a = "shadow";
      print a; // expect: shadow
    }
    print a; // expect: global
    """
)

EXPECTED_STDOUTS = ["shadow", "global"]


def test_shadow_global(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
