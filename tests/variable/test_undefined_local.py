from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/undefined_local.lox
TEST_SRC = dedent(
    """\
    {
      print notDefined;  // expect runtime error: Undefined variable 'notDefined'.
    }
    """
)


def test_undefined_local() -> None:
    interpreter = Lox()

    with pytest.raises(RuntimeError):
        interpreter.run(TEST_SRC)
