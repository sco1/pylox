from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    print str2num("13");  // expect: 13
    print str2num("13.42");  // expect: 13.42
    print str2num("-13");  // expect: -13
    print str2num("-13.42");  // expect: -13.42

    print str2num("foo");  // expect: Cannot convert 'foo' to an integer or float.
    """
)

EXPECTED_STDOUTS = [
    "13",
    "13.42",
    "-13",
    "-13.42",
    "6:20: LoxRuntimeError: Cannot convert 'foo' to an integer or float.",
]


def test_str2num(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
