from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var arr = array(0);
    arr.append(1);
    arr.append(2);
    arr.append(2);
    arr.append(3);

    print mean(arr); // expect: 2

    print median(arr); // expect: 2.0

    print mode(arr);  // expect: 2

    print std(arr); //  expect: 0.816496580927726

    print string_array("abc");  // expect: ["a", "b", "c"]
    """
)

EXPECTED_STDOUTS = [
    "2",
    "2.0",
    "2",
    "0.816496580927726",
    "['a', 'b', 'c']",
]


def test_array_builtins(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
