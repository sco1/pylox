from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/multiply.lox
TEST_SRC = dedent(
    """\
    print 5 * 3; // expect: 15
    print 12.34 * 0.3; // expect: 3.702
    """
)

EXPECTED_STDOUTS = ["15.0", "3.702"]


def test_multiply(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
