from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/missing_comma_in_parameters.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at 'c': Expect ')' after parameters.
    fun foo(a, b c, d, e, f) {}
    """
)

EXPECTED_STDOUTS = ["2:14: LoxParseError: Expected ')' after parameters."]


def test_missing_comma_in_parameters(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
