from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    for (var a = 0; a < 3; a = a + 1) {
        print a;
        break;
    }
    // expect: 0
    """
)

EXPECTED_STDOUTS = ["0"]


def test_for_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
