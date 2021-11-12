from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/not_equals.lox
TEST_SRC = dedent(
    """\
    print nil != nil; // expect: false

    print true != true; // expect: false
    print true != false; // expect: true

    print 1 != 1; // expect: false
    print 1 != 2; // expect: true

    print "str" != "str"; // expect: false
    print "str" != "ing"; // expect: true

    print nil != false; // expect: true
    print false != 0; // expect: true
    print 0 != "0"; // expect: true
    """
)

EXPECTED_STDOUTS = [
    "False",
    "False",
    "True",
    "False",
    "True",
    "False",
    "True",
    "True",
    "True",
    "True",
]


def test_not_equals(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
