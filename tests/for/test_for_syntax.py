from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/syntax.lox
TEST_SRC = dedent(
    """\
    // Single-expression body.
    for (var c = 0; c < 3;) print c = c + 1;
    // expect: 1
    // expect: 2
    // expect: 3

    // Block body.
    for (var a = 0; a < 3; a = a + 1) {
      print a;
    }
    // expect: 0
    // expect: 1
    // expect: 2

    // No clauses.
    fun foo() {
      for (;;) return "done";
    }
    print foo(); // expect: done

    // No variable.
    var i = 0;
    for (; i < 2; i = i + 1) print i;
    // expect: 0
    // expect: 1

    // No condition.
    fun bar() {
      for (var i = 0;; i = i + 1) {
        print i;
        if (i >= 2) return;
      }
    }
    bar();
    // expect: 0
    // expect: 1
    // expect: 2

    // No increment.
    for (var i = 0; i < 2;) {
      print i;
      i = i + 1;
    }
    // expect: 0
    // expect: 1

    // Statement bodies.
    for (; false;) if (true) 1; else 2;
    for (; false;) while (true) 1;
    for (; false;) for (;;) 1;
    """
)

EXPECTED_STDOUTS = [
    "1.0",
    "2.0",
    "3.0",
    "0.0",
    "1.0",
    "2.0",
    "done",
    "0.0",
    "1.0",
    "0.0",
    "1.0",
    "2.0",
    "0.0",
    "1.0",
]


def test_syntax(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
