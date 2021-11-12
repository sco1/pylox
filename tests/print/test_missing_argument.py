from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/print/missing_argument.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at ';': Expect expression.
    print;
    """
)

EXPECTED_STDOUTS = ["2:6: LoxParseError: Expected expression."]


def test_missing_argument(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
