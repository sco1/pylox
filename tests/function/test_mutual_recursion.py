from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/mutual_recursion.lox
TEST_SRC = dedent(
    """\
    fun isEven(n) {
      if (n == 0) return true;
      return isOdd(n - 1);
    }

    fun isOdd(n) {
      if (n == 0) return false;
      return isEven(n - 1);
    }

    print isEven(4); // expect: true
    print isOdd(3); // expect: true
    """
)

EXPECTED_STDOUTS = ["True", "True"]


def test_mutual_recursion(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
