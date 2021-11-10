from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/while/closure_in_body.lox
TEST_SRC = dedent(
    """\
    var f1;
    var f2;
    var f3;

    var i = 1;
    while (i < 4) {
      var j = i;
      fun f() { print j; }

      if (j == 1) f1 = f;
      else if (j == 2) f2 = f;
      else f3 = f;

      i = i + 1;
    }

    f1(); // expect: 1
    f2(); // expect: 2
    f3(); // expect: 3
    """
)

EXPECTED_STDOUTS = ["1.0", "2.0", "3.0"]


@pytest.mark.xfail(reason="Functions not implemented")
def test_closure_in_body(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
