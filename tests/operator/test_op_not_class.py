from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/not_class.lox
TEST_SRC = dedent(
    """\
    class Bar {}
    print !Bar;      // expect: false
    print !Bar();    // expect: false
    """
)

EXPECTED_STDOUTS = ["False", "False"]


def test_not_class(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
