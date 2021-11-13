from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/close_over_method_parameter.lox
TEST_SRC = dedent(
    """\
    var f;

    class Foo {
      method(param) {
        fun f_() {
          print param;
        }
        f = f_;
      }
    }

    Foo().method("param");
    f(); // expect: param
    """
)

EXPECTED_STDOUTS = ["param"]


def test_close_over_method_parameter(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
