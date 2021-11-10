from textwrap import dedent

import pytest

from pylox.lox import Lox

# Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/function/parameters.lox
TEST_SRC = dedent(
    """\
    fun f0() { return 0; }
    print f0(); // expect: 0

    fun f1(a) { return a; }
    print f1(1); // expect: 1

    fun f2(a, b) { return a + b; }
    print f2(1, 2); // expect: 3

    fun f3(a, b, c) { return a + b + c; }
    print f3(1, 2, 3); // expect: 6

    fun f4(a, b, c, d) { return a + b + c + d; }
    print f4(1, 2, 3, 4); // expect: 10

    fun f5(a, b, c, d, e) { return a + b + c + d + e; }
    print f5(1, 2, 3, 4, 5); // expect: 15

    fun f6(a, b, c, d, e, f) { return a + b + c + d + e + f; }
    print f6(1, 2, 3, 4, 5, 6); // expect: 21

    fun f7(a, b, c, d, e, f, g) { return a + b + c + d + e + f + g; }
    print f7(1, 2, 3, 4, 5, 6, 7); // expect: 28

    fun f8(a, b, c, d, e, f, g, h) { return a + b + c + d + e + f + g + h; }
    print f8(1, 2, 3, 4, 5, 6, 7, 8); // expect: 36
    """
)

EXPECTED_STDOUTS = ["0.0", "1.0", "3.0", "6.0", "10.0", "15.0", "21.0", "28.0", "36.0"]


@pytest.mark.xfail(reason="Function returns not implemented")
def test_parameters(capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(TEST_SRC)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.splitlines()
    assert all_out == EXPECTED_STDOUTS
