from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/block/empty.lox
TEST_SRC = dedent(
    """\
    {} // By itself.

    // In a statement.
    if (true) {}
    if (false) {} else {}

    print "ok"; // expect: ok
    """
)

EXPECTED_STDOUTS = ["ok"]


@pytest.mark.xfail(reason="Conditionals/Bool not implemented.")
def test_empty_scope(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
