from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/nested_closure.lox
TEST_SRC = dedent(
    """\
    var f;

    fun f1() {
      var a = "a";
      fun f2() {
        var b = "b";
        fun f3() {
          var c = "c";
          fun f4() {
            print a;
            print b;
            print c;
          }
          f = f4;
        }
        f3();
      }
      f2();
    }
    f1();

    f();
    // expect: a
    // expect: b
    // expect: c
    """
)

EXPECTED_STDOUTS = ["a", "b", "c"]


def test_nested_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
