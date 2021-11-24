from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/number/literals.lox
TEST_SRC = dedent(
    """\
    print 123;     // expect: 123
    print 987654;  // expect: 987654
    print 0;       // expect: 0
    print -0;      // expect: -0

    print 123.456; // expect: 123.456
    print -0.001;  // expect: -0.001
    """
)

EXPECTED_STDOUTS = ["123", "987654", "0", "0", "123.456", "-0.001"]


def test_literals(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
