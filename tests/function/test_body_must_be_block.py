from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/body_must_be_block.lox
TEST_SRC = dedent(
    """\
    // [line 3] Error at '123': Expect '{' before function body.
    fun f() 123;
    """
)

EXPECTED_STDOUTS = ["2:9: LoxParseError: Expected '{' before function body."]


def test_body_must_be_block(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
