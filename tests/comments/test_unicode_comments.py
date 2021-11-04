from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/comments/unicode.lox
TEST_SRC = dedent(
    """\
    // Unicode characters are allowed in comments.
    //
    // Latin 1 Supplement: £§¶ÜÞ
    // Latin Extended-A: ĐĦŋœ
    // Latin Extended-B: ƂƢƩǁ
    // Other stuff: ឃᢆ᯽₪ℜ↩⊗┺░
    // Emoji: ☃☺♣

    print "ok"; // expect: ok
    """
)

EXPECTED_STDOUTS = ["ok"]


def test_unicode_comments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
