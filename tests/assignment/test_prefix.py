from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/prefix_operator.lox
TEST_SRC = dedent(
    """\
    var a = "a";
    !a = "value"; // Error at '=': Invalid assignment target.
    """
)

EXPECTED_STDOUTS = ["2:4: LoxParseError: Invalid assignment target."]


def test_prefix(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
