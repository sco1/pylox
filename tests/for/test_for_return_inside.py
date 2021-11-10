from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/return_inside.lox
TEST_SRC = dedent(
    """\
    fun f() {
      for (;;) {
        var i = "i";
        return i;
      }
    }

    print f();
    // expect: i
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Function returns not implemented")
def test_return_inside(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
