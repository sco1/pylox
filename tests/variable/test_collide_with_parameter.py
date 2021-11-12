from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/collide_with_parameter.lox
TEST_SRC = dedent(
    """\
    fun foo(a) {
      var a; // Error at 'a': Already a variable with this name in this scope.
    }
    """
)

EXPECTED_STDOUTS = ["2:7: LoxResolverError: Variable a already declared in this scope."]


def test_collide_with_parameter(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
