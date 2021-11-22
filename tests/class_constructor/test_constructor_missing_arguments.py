from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/missing_arguments.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init(a, b) {}
    }

    var foo = Foo(1); // expect runtime error: Expected 2 arguments but got 1.
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Constructor not implemented.")
def test_missing_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
