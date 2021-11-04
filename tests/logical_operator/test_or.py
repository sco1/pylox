from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/logical_operator/or.lox
TEST_SRC = dedent(
    """\
    // Note: These tests implicitly depend on ints being truthy.

    // Return the first true argument.
    print 1 or true; // expect: 1
    print false or 1; // expect: 1
    print false or false or true; // expect: true

    // Return the last argument if all are false.
    print false or false; // expect: false
    print false or false or false; // expect: false

    // Short-circuit at the first true argument.
    var a = "before";
    var b = "before";
    (a = false) or
        (b = true) or
        (a = "bad");
    print a; // expect: false
    print b; // expect: true
    """
)

EXPECTED_STDOUTS = ["1.0", "1.0", "True", "False", "False", "False", "True"]


def test_or(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
