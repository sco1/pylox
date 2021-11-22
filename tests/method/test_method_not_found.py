from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/method/not_found.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    Foo().unknown(); // expect runtime error: Undefined property 'unknown'.
    """
)

EXPECTED_STDOUTS = ["3:7: LoxRuntimeError: Undefined property 'unknown'."]


def test_not_found(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
