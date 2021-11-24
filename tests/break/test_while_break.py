from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var a = 0;
    while (a < 3) {
        print a;
        break;
        a = a + 1;
    }
    print a;
    // expect: 0
    // expect: 0
    """
)

EXPECTED_STDOUTS = ["0", "0"]


def test_while_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
