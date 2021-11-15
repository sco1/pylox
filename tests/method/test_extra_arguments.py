from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/method/extra_arguments.lox
TEST_SRC = dedent(
    """\
    class Foo {
      method(a, b) {
        print a;
        print b;
      }
    }

    Foo().method(1, 2, 3, 4); // expect runtime error: Expected 2 arguments but got 4.
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Autogenerated test skeleton")
def test_extra_arguments(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS