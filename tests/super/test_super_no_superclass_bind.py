from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/no_superclass_bind.lox
TEST_SRC = dedent(
    """\
    class Base {
      foo() {
        super.doesNotExist; // Error at 'super': Can't use 'super' in a class with no superclass.
      }
    }

    Base().foo();
    """
)

EXPECTED_STDOUTS = ["3:5: LoxResolverError: Can't use 'super' in a class with no superclass."]


def test_no_superclass_bind(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
