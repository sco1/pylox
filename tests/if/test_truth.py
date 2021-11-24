from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/if/truth.lox
TEST_SRC = dedent(
    """\
    // False and nil are false.
    if (false) print "bad"; else print "false"; // expect: false
    if (nil) print "bad"; else print "nil"; // expect: nil

    // Everything else is true.
    if (true) print true; // expect: true
    if (0) print 0; // expect: 0
    if ("") print "empty"; // expect: empty
    """
)

EXPECTED_STDOUTS = ["false", "nil", "True", "0", "empty"]


def test_truth(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
