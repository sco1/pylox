from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/use_local_in_initializer.lox
TEST_SRC = dedent(
    """\
    var a = "outer";
    {
      var a = a; // Error at 'a': Can't read local variable in its own initializer.
    }
    """
)

EXPECTED_STDOUTS = ["Error at 'a': Can't read local variable in its own initializer."]


@pytest.mark.xfail(reason="Not implemented")
def test_use_local_in_initializer(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
