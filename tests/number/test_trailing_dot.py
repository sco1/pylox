from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/number/trailing_dot.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at ';': Expect property name after '.'.
    123.;
    """
)

EXPECTED_STDOUTS = ["2:4: LoxParseError: Expected ';' after value."]


def test_trailing_dot(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
