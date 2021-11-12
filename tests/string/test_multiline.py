from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/string/multiline.lox
TEST_SRC = dedent(
    """\
    var a = "1
    2
    3";
    print a;
    // expect: 1
    // expect: 2
    // expect: 3
    """
)

EXPECTED_STDOUTS = ["1", "2", "3"]


def test_multiline(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
