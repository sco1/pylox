from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/fun_in_body.lox
TEST_SRC = dedent(
    """\
    // [line 2] Error at 'fun': Expect expression.
    for (;;) fun foo() {}
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Functions not implemented")
def test_fun_in_body(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
