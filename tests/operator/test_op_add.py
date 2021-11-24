from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/add.lox
TEST_SRC = dedent(
    """\
    print 123 + 456; // expect: 579
    print "str" + "ing"; // expect: string
    """
)

EXPECTED_STDOUTS = ["579", "string"]


def test_add(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
