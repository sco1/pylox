from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var arr = array(1);
    arr.append(array(1));
    print arr;

    var arr2 = array(1);
    arr2.append(array(1));
    arr.append(arr2);
    print arr;
    """
)

EXPECTED_STDOUTS = [
    "[nil, [nil]]",
    "[nil, [nil], [nil, [nil]]]",
]


def test_nested_array_print(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
