from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/statement_initializer.lox
TEST_SRC = dedent(
    """\
    // [line 3] Error at '{': Expect expression.
    // [line 3] Error at ')': Expect ';' after expression.
    for ({}; a < 2; a = a + 1) {}
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Autogenerated test skeleton")
def test_statement_initializer(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
