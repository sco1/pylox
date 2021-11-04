from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/logical_operator/or_truth.lox
TEST_SRC = dedent(
    """\
    // False and nil are false.
    print false or "ok"; // expect: ok
    print nil or "ok"; // expect: ok

    // Everything else is true.
    print true or "ok"; // expect: true
    print 0 or "ok"; // expect: 0
    print "s" or "ok"; // expect: s
    """
)

EXPECTED_STDOUTS = ["ok", "ok", "True", "0.0", "s"]


def test_or_truth(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
