from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/inheritance/set_fields_from_base_class.lox
TEST_SRC = dedent(
    """\
    class Foo {
      foo(a, b) {
        this.field1 = a;
        this.field2 = b;
      }

      fooPrint() {
        print this.field1;
        print this.field2;
      }
    }

    class Bar < Foo {
      bar(a, b) {
        this.field1 = a;
        this.field2 = b;
      }

      barPrint() {
        print this.field1;
        print this.field2;
      }
    }

    var bar = Bar();
    bar.foo("foo 1", "foo 2");
    bar.fooPrint();
    // expect: foo 1
    // expect: foo 2

    bar.bar("bar 1", "bar 2");
    bar.barPrint();
    // expect: bar 1
    // expect: bar 2

    bar.fooPrint();
    // expect: bar 1
    // expect: bar 2
    """
)

EXPECTED_STDOUTS = [...]


@pytest.mark.xfail(reason="Inheritance not implemented.")
def test_set_fields_from_base_class(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
