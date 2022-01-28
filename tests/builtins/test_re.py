from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    print re_sub("bar", "", "foobarbaz");

    print re_search("bar", "foobarbaz");
    print re_search("(bar)", "foobarbaz");

    print re_match("foo", "foobarbaz");
    print re_match("(foo)", "foobarbaz");

    print re_findall('f[a-z]*', 'which foot or hand fell fastest');
    print re_findall('f([a-z]*)', 'which foot or hand fell fastest');
    print re_findall('(f)([a-z]*)', 'which foot or hand fell fastest');
    """
)

EXPECTED_STDOUTS = [
    "foobaz",
    "['bar']",
    "['bar', 'bar']",
    "['foo']",
    "['foo', 'foo']",
    "['foot', 'fell', 'fastest']",
    "['oot', 'ell', 'astest']",
    "[['f', 'oot'], ['f', 'ell'], ['f', 'astest']]",
]


def test_regex_builtins(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
