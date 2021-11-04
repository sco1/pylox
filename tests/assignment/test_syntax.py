from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/syntax.lox
TEST_SRC = dedent(
    """\
    // Assignment on RHS of variable.
    var a = "before";
    var c = a = "var";
    print a; // expect: var
    print c; // expect: var
    """
)

EXPECTED_STDOUTS = ["var", "var"]


def test_syntax(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
