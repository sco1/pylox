from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/print/missing_argument.lox
TEST_SRC = dedent(
    """\
    &
    """
)

EXPECTED_STDOUTS = ["1:1: LoxSyntaxError: Unsupported character encountered: '&'"]


def test_missing_argument(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
