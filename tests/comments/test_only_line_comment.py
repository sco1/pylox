from textwrap import dedent

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/comments/only_line_comment.lox
TEST_SRC = dedent(
    """\
    // comment
    """
)


def test_only_line_comment() -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error
