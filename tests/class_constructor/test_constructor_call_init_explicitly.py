from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/call_init_explicitly.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init(arg) {
        print "Foo.init(" + arg + ")";
        this.field = "init";
      }
    }

    var foo = Foo("one"); // expect: Foo.init(one)
    foo.field = "field";

    var foo2 = foo.init("two"); // expect: Foo.init(two)
    print foo2; // expect: Foo instance

    // Make sure init() doesn't create a fresh instance.
    print foo.field; // expect: init
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Constructor not implemented.")
def test_call_init_explicitly(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
