from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/no_superclass_method.lox
TEST_SRC = dedent(
    """\
    class Base {}

    class Derived < Base {
      foo() {
        super.doesNotExist(1); // expect runtime error: Undefined property 'doesNotExist'.
      }
    }

    Derived().foo();
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_no_superclass_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS