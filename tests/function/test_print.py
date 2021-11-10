from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/print.lox
TEST_SRC = dedent(
    """\
    fun foo() {}
    print foo; // expect: <fn foo>

    print clock; // expect: <builtin fn clock>
    """
)

EXPECTED_STDOUTS = ["<fn foo>", "<builtin fn clock>"]


def test_print(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
