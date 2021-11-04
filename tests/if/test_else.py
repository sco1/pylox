from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/if/else.lox
TEST_SRC = dedent(
    """\
    // Evaluate the 'else' expression if the condition is false.
    if (true) print "good"; else print "bad"; // expect: good
    if (false) print "bad"; else print "good"; // expect: good

    // Allow block body.
    if (false) nil; else { print "block"; } // expect: block
    """
)

EXPECTED_STDOUTS = ["good", "good", "block"]


def test_else(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
