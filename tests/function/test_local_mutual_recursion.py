from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/local_mutual_recursion.lox
TEST_SRC = dedent(
    """\
    {
      fun isEven(n) {
        if (n == 0) return true;
        return isOdd(n - 1); // expect runtime error: Undefined variable 'isOdd'.
      }

      fun isOdd(n) {
        if (n == 0) return false;
        return isEven(n - 1);
      }

      isEven(4);
    }
    """
)

EXPECTED_STDOUTS = ["4:12: LoxRuntimeError: Undefined variable 'isOdd'."]


def test_local_mutual_recursion(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
