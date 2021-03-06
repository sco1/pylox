from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var a = 0;
    while (a < 2) {
        print a;
        while (a < 3) {
            print "inner";
            break;
        }
        a = a + 1;
    }
    // expect: 0
    // expect: inner
    // expect: 1
    // expect: inner
    """
)

EXPECTED_STDOUTS = ["0", "inner", "1", "inner"]


def test_nested_while_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
