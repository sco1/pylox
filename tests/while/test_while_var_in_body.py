from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/while/var_in_body.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at 'var': Expect expression.
    while (true) var foo;
    """
)

EXPECTED_STDOUTS = ["2:14: LoxParseError: Expected expression."]


def test_var_in_body(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
