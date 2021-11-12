from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/string/error_after_multiline.lox
TEST_SRC = dedent(
    """\
    // Tests that we correctly track the line info across multiline strings.
    var a = "1
    2
    3
    ";

    err; // // expect runtime error: Undefined variable 'err'.
    """
)

EXPECTED_STDOUTS = ["7:1: LoxRuntimeError: Undefined variable 'err'."]


def test_error_after_multiline(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
