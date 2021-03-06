from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/method/refer_to_name.lox
TEST_SRC = dedent(
    """\
    class Foo {
      method() {
        print method; // expect runtime error: Undefined variable 'method'.
      }
    }

    Foo().method();
    """
)

EXPECTED_STDOUTS = ["3:11: LoxRuntimeError: Undefined variable 'method'."]


def test_refer_to_name(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
