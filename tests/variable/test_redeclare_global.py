from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/redeclare_global.lox
TEST_SRC = dedent(
    """\
    var a = "1";
    var a;
    print a; // expect: nil
    """
)

EXPECTED_STDOUTS = ["nil"]


def test_redeclare_global(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
