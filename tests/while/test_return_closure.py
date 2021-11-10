from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/while/return_closure.lox
TEST_SRC = dedent(
    """\
    fun f() {
      while (true) {
        var i = "i";
        fun g() { print i; }
        return g;
      }
    }

    var h = f();
    h(); // expect: i
    """
)

EXPECTED_STDOUTS = ["i"]


@pytest.mark.xfail(reason="Functions not implemented")
def test_return_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
