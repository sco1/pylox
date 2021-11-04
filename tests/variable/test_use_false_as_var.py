from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/use_false_as_var.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at 'false': Expect variable name.
    var false = "value";
    """
)

EXPECTED_STDOUTS = ["Error at 'false': Expect variable name"]

@pytest.mark.xfail(reason="Not implemented")
def test_use_false_as_var(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
