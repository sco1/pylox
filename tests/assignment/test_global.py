from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/global.lox
TEST_SRC = dedent(
    """\
    var a = "before";
    print a; // expect: before

    a = "after";
    print a; // expect: after

    print a = "arg"; // expect: arg
    print a; // expect: arg
    """
)

EXPECTED_STDOUTS = ["before", "after", "arg", "arg"]


def test_global(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
