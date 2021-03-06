from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/statement_condition.lox
TEST_SRC = dedent(
    """\
    // [line 3] Error at '{': Expect expression.
    // [line 3] Error at ')': Expect ';' after value.
    for (var a = 1; {}; a = a + 1) {}
    """
)

EXPECTED_STDOUTS = [
    "3:17: LoxParseError: Expected expression.",
    "3:30: LoxParseError: Expected ';' after value.",
]


def test_statement_condition(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
