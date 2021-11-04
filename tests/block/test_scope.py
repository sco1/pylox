from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/block/scope.lox
TEST_SRC = dedent(
    """\
    var a = "outer";

    {
    var a = "inner";
    print a; // expect: inner
    }

    print a; // expect: outer
    """
)

EXPECTED_STDOUTS = ["inner", "outer"]


def test_scope(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
