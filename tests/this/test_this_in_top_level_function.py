from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/this/this_in_top_level_function.lox
TEST_SRC = dedent(
    """\
    fun foo() {
      this; // Error at 'this': Can't use 'this' outside of a class.
    }
    """
)

EXPECTED_STDOUTS = ["2:3: LoxResolverError: Can't use 'this' outside of a class."]


def test_this_in_top_level_function(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
