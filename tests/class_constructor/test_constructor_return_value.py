from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/return_value.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init() {
        return "result"; // Error at 'return': Can't return a value from an initializer.
      }
    }
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Constructor not implemented.")
def test_return_value(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
