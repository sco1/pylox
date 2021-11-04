from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/in_middle_of_block.lox
TEST_SRC = dedent(
    """\
    {
      var a = "a";
      print a; // expect: a
      var b = a + " b";
      print b; // expect: a b
      var c = a + " c";
      print c; // expect: a c
      var d = b + " d";
      print d; // expect: a b d
    }
    """
)

EXPECTED_STDOUTS = ["a", "a b", "a c", "a b d"]


def test_in_middle_of_block(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
