from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/field/on_instance.lox
TEST_SRC = dedent(
    """\
    class Foo {}

    var foo = Foo();

    print foo.bar = "bar value"; // expect: bar value
    print foo.baz = "baz value"; // expect: baz value

    print foo.bar; // expect: bar value
    print foo.baz; // expect: baz value
    """
)

EXPECTED_STDOUTS = ["bar value", "baz value", "bar value", "baz value"]


def test_on_instance(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
