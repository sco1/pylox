from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/local_from_method.lox
TEST_SRC = dedent(
    """\
    var foo = "variable";

    class Foo {
      method() {
        print foo;
      }
    }

    Foo().method(); // expect: variable
    """
)

EXPECTED_STDOUTS = ["variable"]


@pytest.mark.xfail(reason="Classes not implemented")
def test_local_from_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
