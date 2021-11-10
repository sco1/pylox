from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/number/leading_dot.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at '.': Expect expression.
    .123;
    """
)

EXPECTED_STDOUTS = ["Error at '.': Expect expression."]


@pytest.mark.xfail(reason="Not implemented")
def test_leading_dot(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
