from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/class/inherit_self.lox
TEST_SRC = dedent(
    """\
    class Foo < Foo {} // Error at 'Foo': A class can't inherit from itself.
    """
)

EXPECTED_STDOUTS = ["1:13: LoxResolverError: Class cannot inherit from itself."]


def test_inherit_self(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
