from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/return/in_method.lox
TEST_SRC = dedent(
    """\
    class Foo {
      method() {
        return "ok";
        print "bad";
      }
    }

    print Foo().method(); // expect: ok
    """
)

EXPECTED_STDOUTS = ["ok"]


@pytest.mark.xfail(reason="Classes not implemented")
def test_in_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
