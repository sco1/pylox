import pytest

from pylox.lox import Lox

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/bool/not.lox
TEST_CASES = [
    ("print !true;", False),
    ("print !false;", True),
    ("print !!true;", True),
]


@pytest.mark.parametrize("src, truth_val", TEST_CASES)
def test_not(src: str, truth_val: bool, capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(src)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.strip()
    assert all_out == str(truth_val)
