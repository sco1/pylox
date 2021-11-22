from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/equals_method.lox
TEST_SRC = dedent(
    """\
    // Bound methods have identity equality.
    class Foo {
      method() {}
    }

    var foo = Foo();
    var fooMethod = foo.method;

    // Same bound method.
    print fooMethod == fooMethod; // expect: true

    // Different closurizations.
    print foo.method == foo.method; // expect: true
    """
)

EXPECTED_STDOUTS = ["True", "True"]


def test_equals_method(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
