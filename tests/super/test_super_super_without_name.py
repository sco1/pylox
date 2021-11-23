from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/super_without_name.lox
TEST_SRC = dedent(
    """\
    class A {}

    class B < A {
      method() {
        super.; // Error at ';': Expect superclass method name.
      }
    }
    """
)

EXPECTED_STDOUTS = ["5:11: LoxParseError: Expected superclass method name."]


def test_super_without_name(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
