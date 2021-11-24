from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/negate.lox
TEST_SRC = dedent(
    """\
    print -(3); // expect: -3
    print --(3); // expect: 3
    print ---(3); // expect: -3
    """
)

EXPECTED_STDOUTS = ["-3", "3", "-3"]


def test_negate(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
