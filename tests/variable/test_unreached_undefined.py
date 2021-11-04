from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/variable/unreached_undefined.lox
TEST_SRC = dedent(
    """\
    if (false) {
      print notDefined;
    }

    print "ok"; // expect: ok
    """
)

EXPECTED_STDOUTS = ["ok"]


def test_unreached_undefined(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
