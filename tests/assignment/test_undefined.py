from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/assignment/undefined.lox
TEST_SRC = dedent(
    """\
    unknown = "what"; // expect runtime error: Undefined variable 'unknown'.
    """
)


def test_to_this() -> None:
    interpreter = Lox()

    with pytest.raises(RuntimeError):
        interpreter.run(TEST_SRC)
