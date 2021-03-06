from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/method/empty_block.lox
TEST_SRC = dedent(
    """\
    class Foo {
      bar() {}
    }

    print Foo().bar(); // expect: nil
    """
)

EXPECTED_STDOUTS = ["nil"]


def test_empty_block(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
