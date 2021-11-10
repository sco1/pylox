from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/while/syntax.lox
TEST_SRC = dedent(
    """\
    // Single-expression body.
    var c = 0;
    while (c < 3) print c = c + 1;
    // expect: 1
    // expect: 2
    // expect: 3

    // Block body.
    var a = 0;
    while (a < 3) {
      print a;
      a = a + 1;
    }
    // expect: 0
    // expect: 1
    // expect: 2

    // Statement bodies.
    while (false) if (true) 1; else 2;
    while (false) while (true) 1;
    while (false) for (;;) 1;
    """
)

EXPECTED_STDOUTS = ["1.0", "2.0", "3.0", "0.0", "1.0", "2.0"]


def test_syntax(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
