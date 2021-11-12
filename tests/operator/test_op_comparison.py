from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/comparison.lox
TEST_SRC = dedent(
    """\
    print 1 < 2;    // expect: true
    print 2 < 2;    // expect: false
    print 2 < 1;    // expect: false

    print 1 <= 2;    // expect: true
    print 2 <= 2;    // expect: true
    print 2 <= 1;    // expect: false

    print 1 > 2;    // expect: false
    print 2 > 2;    // expect: false
    print 2 > 1;    // expect: true

    print 1 >= 2;    // expect: false
    print 2 >= 2;    // expect: true
    print 2 >= 1;    // expect: true

    // Zero and negative zero compare the same.
    print 0 < -0; // expect: false
    print -0 < 0; // expect: false
    print 0 > -0; // expect: false
    print -0 > 0; // expect: false
    print 0 <= -0; // expect: true
    print -0 <= 0; // expect: true
    print 0 >= -0; // expect: true
    print -0 >= 0; // expect: true
    """
)

EXPECTED_STDOUTS = [
    "True",
    "False",
    "False",
    "True",
    "True",
    "False",
    "False",
    "False",
    "True",
    "False",
    "True",
    "True",
    "False",
    "False",
    "False",
    "False",
    "True",
    "True",
    "True",
    "True",
]


def test_comparison(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
