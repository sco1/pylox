from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/inherit_methods.lox
TEST_SRC = dedent(
    """\
    class Foo {
      methodOnFoo() { print "foo"; }
      override() { print "foo"; }
    }

    class Bar < Foo {
      methodOnBar() { print "bar"; }
      override() { print "bar"; }
    }

    var bar = Bar();
    bar.methodOnFoo(); // expect: foo
    bar.methodOnBar(); // expect: bar
    bar.override(); // expect: bar
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_inherit_methods(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
