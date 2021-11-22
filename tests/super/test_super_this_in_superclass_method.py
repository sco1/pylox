from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/this_in_superclass_method.lox
TEST_SRC = dedent(
    """\
    class Base {
      init(a) {
        this.a = a;
      }
    }

    class Derived < Base {
      init(a, b) {
        super.init(a);
        this.b = b;
      }
    }

    var derived = Derived("a", "b");
    print derived.a; // expect: a
    print derived.b; // expect: b
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_this_in_superclass_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
