from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/parenthesized_superclass.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    // [line 4] Error at '(': Expect superclass name.
    class Bar < (Foo) {}
    """
)

EXPECTED_STDOUTS = ["4:13: LoxParseError: Expected superclass name."]


def test_parenthesized_superclass(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
