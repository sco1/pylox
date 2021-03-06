from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      bar(arg) {
        print arg;
      }
    }

    var bar = Foo().bar;
    print "got method"; // expect: got method
    bar("arg");          // expect: arg
    """
)

EXPECTED_STDOUTS = ["got method", "arg"]


def test_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
