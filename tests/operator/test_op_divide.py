from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/divide.lox
TEST_SRC = dedent(
    """\
    print 8 / 2;          // expect: 4.0
    print 12.34 / 12.34;  // expect: 1.0
    print 1 / 0;          // expect: "nan"
    print 10 \\ 3;        // expect: 3
    print 12.5 \\ 4;      // expect: 3.0
    print 1 \\ 0;         // expect: "nan"
    """
)

EXPECTED_STDOUTS = ["4.0", "1.0", "nan", "3", "3.0", "nan"]


def test_divide(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
