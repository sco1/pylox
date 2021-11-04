from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/scope_reuse_in_different_blocks.lox
TEST_SRC = dedent(
    """\
    {
      var a = "first";
      print a; // expect: first
    }

    {
      var a = "second";
      print a; // expect: second
    }
    """
)

EXPECTED_STDOUTS = ["first", "second"]


def test_scope_reuse_in_different_blocks(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
