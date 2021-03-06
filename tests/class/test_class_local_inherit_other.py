from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/class/local_inherit_other.lox
TEST_SRC = dedent(
    """\
    class A {}

    fun f() {
      class B < A {}
      return B;
    }

    print f(); // expect: B
    """
)

EXPECTED_STDOUTS = ["<cls B>"]


def test_local_inherit_other(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
