import pytest

from pylox.lox import Lox

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/bool/equality.lox
# None and False are falsy, everything else is Truthy
TEST_CASES = [
    # Equal
    ("print true == true;", True),
    ("print true == false;", False),
    ("print false == true;", False),
    ("print false == false;", True),
    # Not equal to other types
    ("print true == 1;", False),
    ("print false == 0;", False),
    ("print true == 'true';", False),
    ("print false == 'false';", False),
    ("print false == '';", False),
    # Not equal
    ("print true != true;", False),
    ("print true != false;", True),
    ("print false != true;", True),
    ("print false != false;", False),
    # Not equal to other types
    ("print true != 1;", True),
    ("print false != 0;", True),
    ("print true != 'true';", True),
    ("print false != 'false';", True),
    ("print false != '';", True),
]


@pytest.mark.parametrize("src, truth_val", TEST_CASES)
def test_equality(src: str, truth_val: bool, capsys: pytest.CaptureFixture) -> None:
    interpreter = Lox()
    interpreter.run(src)

    assert not interpreter.had_error
    assert not interpreter.had_runtime_error

    all_out = capsys.readouterr().out.strip()
    assert all_out == str(truth_val)
