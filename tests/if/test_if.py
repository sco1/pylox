from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/if/if.lox
TEST_SRC = dedent(
    """\
    // Evaluate the 'then' expression if the condition is true.
    if (true) print "good"; // expect: good
    if (false) print "bad";

    // Allow block body.
    if (true) { print "block"; } // expect: block

    // Assignment in if condition.
    var a = false;
    if (a = true) print a; // expect: true
    """
)

EXPECTED_STDOUTS = ["good", "block", "True"]


def test_if(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
