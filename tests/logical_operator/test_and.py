from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/logical_operator/and.lox
TEST_SRC = dedent(
    """\
    // Note: These tests implicitly depend on ints being truthy.

    // Return the first non-true argument.
    print false and 1; // expect: false
    print true and 1; // expect: 1
    print 1 and 2 and false; // expect: false

    // Return the last argument if all are true.
    print 1 and true; // expect: true
    print 1 and 2 and 3; // expect: 3

    // Short-circuit at the first false argument.
    var a = "before";
    var b = "before";
    (a = true) and
        (b = false) and
        (a = "bad");
    print a; // expect: true
    print b; // expect: false
    """
)

EXPECTED_STDOUTS = ["False", "1", "False", "True", "3", "True", "False"]


def test_and(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
