from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/if/dangling_else.lox
TEST_SRC = dedent(
    """\
    // A dangling else binds to the right-most if.
    if (true) if (false) print "bad"; else print "good"; // expect: good
    if (false) if (true) print "bad"; else print "bad";
    """
)

EXPECTED_STDOUTS = ["good"]


def test_dangling_else(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
