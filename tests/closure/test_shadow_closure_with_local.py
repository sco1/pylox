from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/shadow_closure_with_local.lox
TEST_SRC = dedent(
    """\
    {
      var foo = "closure";
      fun f() {
        {
          print foo; // expect: closure
          var foo = "shadow";
          print foo; // expect: shadow
        }
        print foo; // expect: closure
      }
      f();
    }
    """
)

EXPECTED_STDOUTS = ["closure", "shadow", "closure"]


def test_shadow_closure_with_local(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
