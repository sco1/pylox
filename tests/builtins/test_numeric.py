from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    print abs(13);  // expect: 13
    print abs(-13);  // expect: 13

    print ceil(13.42);  // expect: 14
    print ceil(-13.42);  // expect: -13

    print divmod(13, 7); // expect [1, 6]

    print floor(13.42);  // expect: 13
    print floor(-13.42);  // expect: -14

    print max(7, 13);  // expect: 13
    print max(13, 7);  // expect: 13

    print min(7, 13);  // expect: 7
    print min(13, 7);  // expect: 7

    print ord("a");  // expect: 97
    """
)

EXPECTED_STDOUTS = [
    "13",
    "13",
    "14",
    "-13",
    "[1, 6]",
    "13",
    "-14",
    "13",
    "13",
    "7",
    "7",
    "97",
]


def test_numeric_builtins(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
