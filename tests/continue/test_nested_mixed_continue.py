from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    var a = 0;
    while (a < 2) {
        print a;
        for (var b = 10; b < 12; b = b + 1) {
            print "inner";
            if (b == 11) continue; else print b;
        }
        a = a + 1;
    }
    // expect: 0
    // expect: inner
    // expect: 10
    // expect: 1
    // expect: inner
    // expect: 10
    """
)

EXPECTED_STDOUTS = ["0", "inner", "10", "1", "inner", "10"]


@pytest.mark.xfail(reason="Continue not implemented.")
def test_nested_mixed_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
