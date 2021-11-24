from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/precedence.lox
TEST_SRC = dedent(
    """\
    // * has higher precedence than +.
    print 2 + 3 * 4; // expect: 14

    // * has higher precedence than -.
    print 20 - 3 * 4; // expect: 8

    // / has higher precedence than +.
    print 2 + 6 / 3; // expect: 4.0

    // / has higher precedence than -.
    print 2 - 6 / 3; // expect: 0.0

    // < has higher precedence than ==.
    print false == 2 < 1; // expect: true

    // > has higher precedence than ==.
    print false == 1 > 2; // expect: true

    // <= has higher precedence than ==.
    print false == 2 <= 1; // expect: true

    // >= has higher precedence than ==.
    print false == 1 >= 2; // expect: true

    // 1 - 1 is not space-sensitive.
    print 1 - 1; // expect: 0
    print 1 -1;  // expect: 0
    print 1- 1;  // expect: 0
    print 1-1;   // expect: 0

    // Using () for grouping.
    print (2 * (6 - (2 + 2))); // expect: 4
    """
)

EXPECTED_STDOUTS = [
    "14",
    "8",
    "4.0",
    "0.0",
    "True",
    "True",
    "True",
    "True",
    "0",
    "0",
    "0",
    "0",
    "4",
]


def test_precedence(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
