from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/call_init_early_return.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init() {
        print "init";
        return;
        print "nope";
      }
    }

    var foo = Foo(); // expect: init
    print foo.init(); // expect: init
    // expect: Foo instance
    """
)

EXPECTED_STDOUTS = ["init", "init", "<inst Foo>"]


def test_call_init_early_return(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
