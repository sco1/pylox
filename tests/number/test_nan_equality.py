from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/number/nan_equality.lox
TEST_SRC = dedent(
    """\
    var nan = 0/0;

    print nan == 0; // expect: false
    print nan != 1; // expect: true

    // NaN is not equal to self.
    print nan == nan; // expect: false
    print nan != nan; // expect: true
    """
)

EXPECTED_STDOUTS = ["False", "True", "False", "True"]


def test_nan_equality(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
