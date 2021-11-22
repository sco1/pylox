from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/reassign_superclass.lox
TEST_SRC = dedent(
    """\
    class Base {
      method() {
        print "Base.method()";
      }
    }

    class Derived < Base {
      method() {
        super.method();
      }
    }

    class OtherBase {
      method() {
        print "OtherBase.method()";
      }
    }

    var derived = Derived();
    derived.method(); // expect: Base.method()
    Base = OtherBase;
    derived.method(); // expect: Base.method()
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_reassign_superclass(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
