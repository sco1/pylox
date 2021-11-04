import pytest
import pytest_check as check

from pylox.lox import Lox
from pylox.parser import Parser
from pylox.scanner import Scanner

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/expressions/evaluate.lox
EVALUATION_PARSING_CASES = [
    ("(5 - (3 - 1)) + -1", 2),
]


@pytest.mark.xfail(reason="Not updated for new interpreter flow")
@pytest.mark.parametrize(("in_src", "truth_value"), EVALUATION_PARSING_CASES)
def test_expression_parsing(in_src: str, truth_value: float) -> None:
    interpreter = Lox()
    scanner = Scanner(in_src, interpreter)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, interpreter)
    expr = parser.parse()

    check.is_false(interpreter.had_error)

    _, val = interpreter.interpreter.interpret(expr)
    check.equal(val, truth_value)
