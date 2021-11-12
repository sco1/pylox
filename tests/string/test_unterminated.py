from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/string/unterminated.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error: Unterminated string.
    "this string has no close quote
    """
)

EXPECTED_STDOUTS = ["3:1: LoxSyntaxError: Unterminated string."]


def test_unterminated(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
