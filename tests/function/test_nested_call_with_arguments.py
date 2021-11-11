from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/nested_call_with_arguments.lox
TEST_SRC = dedent(
    """\
    fun returnArg(arg) {
      return arg;
    }

    fun returnFunCallWithArg(func, arg) {
      return returnArg(func)(arg);
    }

    fun printArg(arg) {
      print arg;
    }

    returnFunCallWithArg(printArg, "hello world"); // expect: hello world
    """
)

EXPECTED_STDOUTS = ["hello world"]


def test_nested_call_with_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
