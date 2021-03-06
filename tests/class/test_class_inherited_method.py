from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/class/inherited_method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      inFoo() {
        print "in foo";
      }
    }

    class Bar < Foo {
      inBar() {
        print "in bar";
      }
    }

    class Baz < Bar {
      inBaz() {
        print "in baz";
      }
    }

    var baz = Baz();
    baz.inFoo(); // expect: in foo
    baz.inBar(); // expect: in bar
    baz.inBaz(); // expect: in baz
    """
)

EXPECTED_STDOUTS = ["in foo", "in bar", "in baz"]


def test_inherited_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
