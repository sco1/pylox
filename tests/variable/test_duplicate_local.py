from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/duplicate_local.lox
TEST_SRC = dedent(
    """\
    {
      var a = "value";
      var a = "other"; // Error at 'a': Already a variable with this name in this scope.
    }
    """
)


def test_duplicate_local() -> None:
    interpreter = Lox()

    with pytest.raises(RuntimeError):
        interpreter.run(TEST_SRC)
