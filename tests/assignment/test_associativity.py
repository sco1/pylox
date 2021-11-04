from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/associativity.lox
TEST_SRC = dedent(
    """\
    var a = "a";
    var b = "b";
    var c = "c";

    // Assignment is right-associative.
    a = b = c;
    print a; // expect: c
    print b; // expect: c
    print c; // expect: c
    """
)

EXPECTED_STDOUTS = ["c", "c", "c"]


def test_associativity(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
