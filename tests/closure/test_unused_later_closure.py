from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/closure/unused_later_closure.lox
TEST_SRC = dedent(
    """\
    // This is a regression test. When closing upvalues for discarded locals, it
    // wouldn't make sure it discarded the upvalue for the correct stack slot.
    //
    // Here we create two locals that can be closed over, but only the first one
    // actually is. When "b" goes out of scope, we need to make sure we don't
    // prematurely close "a".
    var closure;

    {
      var a = "a";

      {
        var b = "b";
        fun returnA() {
          return a;
        }

        closure = returnA;

        if (false) {
          fun returnB() {
            return b;
          }
        }
      }

      print closure(); // expect: a
    }
    """
)

EXPECTED_STDOUTS = ["a"]


def test_unused_later_closure(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
