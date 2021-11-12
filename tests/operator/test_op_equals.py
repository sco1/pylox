from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/equals.lox
TEST_SRC = dedent(
    """\
    print nil == nil; // expect: true

    print true == true; // expect: true
    print true == false; // expect: false

    print 1 == 1; // expect: true
    print 1 == 2; // expect: false

    print "str" == "str"; // expect: true
    print "str" == "ing"; // expect: false

    print nil == false; // expect: false
    print false == 0; // expect: false
    print 0 == "0"; // expect: false
    """
)

EXPECTED_STDOUTS = [
    "True",
    "True",
    "False",
    "True",
    "False",
    "True",
    "False",
    "False",
    "False",
    "False",
]


def test_equals(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
