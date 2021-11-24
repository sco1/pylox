from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    print 2^3;      // expect: 8
    print 2.0^3;    // expect: 8.0
    print 4^(1/2);  // expect: 2.0
    print 4^(0.5);  // expect: 2.0
    """
)

EXPECTED_STDOUTS = ["8", "8.0", "2.0", "2.0"]


def test_power(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
