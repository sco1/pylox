from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/for/closure_in_body.lox
TEST_SRC = dedent(
    """\
    var f1;
    var f2;
    var f3;

    for (var i = 1; i < 4; i = i + 1) {
      var j = i;
      fun f() {
        print i;
        print j;
      }

      if (j == 1) f1 = f;
      else if (j == 2) f2 = f;
      else f3 = f;
    }

    f1(); // expect: 4
          // expect: 1
    f2(); // expect: 4
          // expect: 2
    f3(); // expect: 4
          // expect: 3
    """
)

EXPECTED_STDOUTS = ["4", "1", "4", "2", "4", "3"]


def test_closure_in_body(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
