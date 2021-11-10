from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/early_bound.lox
TEST_SRC = dedent(
    """\
    var a = "outer";
    {
      fun foo() {
        print a;
      }

      foo(); // expect: outer
      var a = "inner";
      foo(); // expect: outer
    }
    """
)

EXPECTED_STDOUTS = ["outer", "outer", "outer"]


@pytest.mark.xfail(reason="Functions not implemented")
def test_early_bound(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
