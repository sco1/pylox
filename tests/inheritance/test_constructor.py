from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/constructor.lox
TEST_SRC = dedent(
    """\
    class A {
      init(param) {
        this.field = param;
      }

      test() {
        print this.field;
      }
    }

    class B < A {}

    var b = B("value");
    b.test(); // expect: value
    """
)

EXPECTED_STDOUTS = ["value"]


def test_constructor(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
