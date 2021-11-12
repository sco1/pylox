from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/not.lox
TEST_SRC = dedent(
    """\
    print !true;     // expect: false
    print !false;    // expect: true
    print !!true;    // expect: true

    print !123;      // expect: false
    print !0;        // expect: false

    print !nil;     // expect: true

    print !"";       // expect: false

    fun foo() {}
    print !foo;      // expect: false
    """
)

EXPECTED_STDOUTS = ["False", "True", "True", "False", "False", "True", "False", "False"]


def test_not(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
