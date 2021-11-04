from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/in_nested_block.lox
TEST_SRC = dedent(
    """\
    {
      var a = "outer";
      {
        print a; // expect: outer
      }
    }
    """
)

EXPECTED_STDOUTS = ["outer"]


def test_in_nested_block(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
