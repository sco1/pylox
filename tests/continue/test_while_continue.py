from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var a = 0;
    while (a < 3) {
        if (a == 2) {
            a = a + 1;
            continue;
        }
        else {
            print a;
            a = a + 1;
        }
    }
    // expect: 0
    // expect: 1
    """
)

EXPECTED_STDOUTS = ["0", "1"]


@pytest.mark.xfail(reason="Continue not implemented.")
def test_while_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
