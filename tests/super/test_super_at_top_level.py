from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/super/super_at_top_level.lox
TEST_SRC = dedent(
    """\
    super.foo("bar"); // Error at 'super': Can't use 'super' outside of a class.
    super.foo; // Error at 'super': Can't use 'super' outside of a class.
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Autogenerated test skeleton")
def test_super_at_top_level(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
