from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var a = "abc123";
    print len(a);  // expect: 6

    var arr = array(0);
    arr.append(1);
    arr.append(2);
    arr.append(2);
    arr.append(3);

    print len(arr);  // expect: 4

    print len(42);  // expect: Object of type 'int' has no length.
    """
)

EXPECTED_STDOUTS = ["6", "4", "12:13: LoxRuntimeError: Object of type 'int' has no length."]


def test_len_builtin(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
