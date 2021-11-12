from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/return/at_top_level.lox
TEST_SRC = dedent(
    """\
    return "wat"; // Error at 'return': Can't return from top-level code.
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Not implemented")
def test_at_top_level(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
