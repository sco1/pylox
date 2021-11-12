from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/string/literals.lox
TEST_SRC = dedent(
    """\
    print "(" + "" + ")";   // expect: ()
    print "a string"; // expect: a string

    // Non-ASCII.
    print "A~¶Þॐஃ"; // expect: A~¶Þॐஃ
    """
)

EXPECTED_STDOUTS = ["()", "a string", "A~¶Þॐஃ"]


def test_literals(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
