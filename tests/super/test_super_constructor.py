from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/constructor.lox
TEST_SRC = dedent(
    """\
    class Base {
      init(a, b) {
        print "Base.init(" + a + ", " + b + ")";
      }
    }

    class Derived < Base {
      init() {
        print "Derived.init()";
        super.init("a", "b");
      }
    }

    Derived();
    // expect: Derived.init()
    // expect: Base.init(a, b)
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_constructor(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
