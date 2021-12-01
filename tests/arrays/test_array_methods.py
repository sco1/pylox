from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var arr = array(1);
    print arr;  // expect: [nil]

    arr.append("foo");
    print arr;  // expect: [nil, 'foo']

    arr.appendleft("bar");
    print arr;  // expect: ['bar', nil, 'foo']

    arr.reverse();
    print arr;  // expect: ['foo', nil, 'bar']

    var a = arr.pop();
    print a;  // expect: bar
    print arr;  // expect: ['foo', nil]

    var b = arr.popleft();
    print b;  // expect: foo
    print arr;  // expect: [nil]

    arr.clear();
    print arr; // expect: []

    arr.append("foo");
    arr.append("bar");
    print arr.join(""); // expect: "foobar"
    """
)

EXPECTED_STDOUTS = [
    "[nil]",
    "[nil, 'foo']",
    "['bar', nil, 'foo']",
    "['foo', nil, 'bar']",
    "bar",
    "['foo', nil]",
    "foo",
    "[nil]",
    "[]",
    "foobar",
]


def test_array_printing(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
