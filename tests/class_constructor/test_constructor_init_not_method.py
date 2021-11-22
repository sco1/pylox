from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/constructor/init_not_method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      init(arg) {
        print "Foo.init(" + arg + ")";
        this.field = "init";
      }
    }

    fun init() {
      print "not initializer";
    }

    init(); // expect: not initializer
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Constructor not implemented.")
def test_init_not_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
