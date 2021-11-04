from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/redefine_global.lox
TEST_SRC = dedent(
    """\
    var a = "1";
    var a = "2";
    print a; // expect: 2
    """
)

EXPECTED_STDOUTS = ["2"]


def test_redefine_global(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
