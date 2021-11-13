from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/operator/equals_class.lox
TEST_SRC = dedent(
    """\
    // Bound methods have identity equality.
    class Foo {}
    class Bar {}

    print Foo == Foo; // expect: true
    print Foo == Bar; // expect: false
    print Bar == Foo; // expect: false
    print Bar == Bar; // expect: true

    print Foo == "Foo"; // expect: false
    print Foo == nil;   // expect: false
    print Foo == 123;   // expect: false
    print Foo == true;  // expect: false
    """
)

EXPECTED_STDOUTS = ["True", "False", "False", "True", "False", "False", "False", "False"]


def test_equals_class(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
