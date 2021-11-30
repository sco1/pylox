from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var arr = array(0);
    arr.pop();  // expect: LoxRuntimeError
    """
)

EXPECTED_STDOUTS = ["2:5: LoxRuntimeError: Cannot pop from empty array."]


def test_empty_pop(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
