from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/recursion.lox
TEST_SRC = dedent(
    """\
    fun fib(n) {
      if (n < 2) return n;
      return fib(n - 1) + fib(n - 2);
    }

    print fib(8); // expect: 21
    """
)

EXPECTED_STDOUTS = ["21.0"]


@pytest.mark.xfail(reason="Function returns not implemented")
def test_recursion(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
