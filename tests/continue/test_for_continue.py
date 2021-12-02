from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    for (var a = 0; a < 3; a = a + 1) {
        if (a == 1) continue; else print a;
    }
    // expect: 0
    // expect: 2
    """
)

EXPECTED_STDOUTS = ["0", "2"]


@pytest.mark.xfail(reason="Continue not implemented.")
def test_for_continue(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
