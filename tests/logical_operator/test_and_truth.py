from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/logical_operator/and_truth.lox
TEST_SRC = dedent(
    """\
    // False and nil are false.
    print false and "bad"; // expect: false
    print nil and "bad"; // expect: nil

    // Everything else is true.
    print true and "ok"; // expect: ok
    print 0 and "ok"; // expect: ok
    print "" and "ok"; // expect: ok
    """
)

EXPECTED_STDOUTS = ["False", "nil", "ok", "ok", "ok"]


def test_and_truth(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
