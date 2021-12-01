from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    print str2num("13");  // expect: 13
    print str2num("13.42");  // expect: 13.42
    print str2num("-13");  // expect: -13
    print str2num("-13.42");  // expect: -13.42
    """
)

EXPECTED_STDOUTS = [
    "13",
    "13.42",
    "-13",
    "-13.42",
]


def test_str2num(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
