from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/get_on_nil.lox
TEST_SRC = dedent(
    """\
    nil.foo; // expect runtime error: Only instances have properties.
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Autogenerated test skeleton")
def test_get_on_nil(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
