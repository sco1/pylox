from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/statement_increment.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at '{': Expect expression.
    for (var a = 1; a < 2; {}) {}
    """
)

EXPECTED_STDOUTS = ["2:24: LoxParseError: Expected expression."]


def test_statement_increment(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
