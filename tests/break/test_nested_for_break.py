from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    for (var a = 0; a < 2; a = a + 1) {
        print a;

        for (var b = 0; b < 3; b = b + 1) {
            print "inner";
            break;
        }
    }
    // expect: 0
    // expect: inner
    // expect: 1
    // expect: inner
    """
)

EXPECTED_STDOUTS = ["0.0", "inner", "1.0", "inner"]


def test_nested_for_break(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
