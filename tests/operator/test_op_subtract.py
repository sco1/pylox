from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/subtract.lox
TEST_SRC = dedent(
    """\
    print 4 - 3; // expect: 1
    print 1.2 - 1.2; // expect: 0
    """
)

EXPECTED_STDOUTS = ["1.0", "0.0"]


def test_subtract(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
