from textwrap import dedent

import pytest

from pylox.preprocessor import PreProcessor

STDLIB_INCLUDE = dedent(
    """\
    include <hello_world>
    """
)

HELLO_WORLD = dedent(
    """\
    fun hello_world() {
        print "Hello, world!";
    }
    """
)


def test_stdlib_include() -> None:
    pre = PreProcessor(STDLIB_INCLUDE)
    assert pre.resolved_src == HELLO_WORLD


PATH_INCLUDE = dedent(
    """\
    include "./pylox/builtins/hello_world.lox"
    """
)


def test_path_include() -> None:
    pre = PreProcessor(PATH_INCLUDE)
    assert pre.resolved_src == HELLO_WORLD


NONEXISTENT_INCLUDE = dedent(
    """\
    include <butts>
    """
)


def test_nonexistent_include() -> None:
    with pytest.raises(ValueError):
        PreProcessor(NONEXISTENT_INCLUDE)


BLANK_LINE_IN_INCLUDE = dedent(
    """\
    include <hello_world>

    include <hello_world>
    """
)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_blank_line_in_include() -> None:
    pre = PreProcessor(BLANK_LINE_IN_INCLUDE)
    assert pre.resolved_src == f"{HELLO_WORLD}\n{HELLO_WORLD}"


def test_duplicate_include_warns() -> None:
    with pytest.warns(UserWarning):
        PreProcessor(BLANK_LINE_IN_INCLUDE)


INCLUDE_BREAK = dedent(
    """\
    include <hello_world>
    foo
    include <hello_world>
    """
)


def test_include_break() -> None:
    pre = PreProcessor(INCLUDE_BREAK)
    assert pre.resolved_src == f"{HELLO_WORLD}foo\ninclude <hello_world>\n"
