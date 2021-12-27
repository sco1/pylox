from textwrap import dedent

import pytest

from pylox.lox import Lox

TEST_SRC = dedent(
    """\
    continue; // Expect resolver error: Can't use 'continue' outside of a for or while loop.
    """
)

EXPECTED_STDOUTS = ["1:1: LoxResolverError: Can't use 'continue' outside of a for or while loop."]


def test_global_continue(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS