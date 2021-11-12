from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/return/return_nil_if_no_value.lox
TEST_SRC = dedent(
    """\
    fun f() {
      return;
      print "bad";
    }

    print f(); // expect: nil
    """
)

EXPECTED_STDOUTS = ["nil"]


def test_return_nil_if_no_value(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
