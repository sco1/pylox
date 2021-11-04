import pytest
import pytest_check as check

from pylox.ast_printer import AstPrinter
from pylox.lox import Lox
from pylox.parser import Parser
from pylox.scanner import Scanner

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/expressions/parse.lox
EXPRESSION_PARSING_CASES = [
    ("(5 - (3 - 1)) + -1", "(+ (group (- 5.0 (group (- 3.0 1.0)))) (- 1.0))"),
]


@pytest.mark.xfail(reason="AST printer needs updating for new grammar")
@pytest.mark.parametrize(("in_src", "truth_ast"), EXPRESSION_PARSING_CASES)
def test_expression_parsing(in_src: str, truth_ast: str) -> None:
    interpreter = Lox()
    scanner = Scanner(in_src, interpreter)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, interpreter)
    expr = parser.parse()

    check.is_false(interpreter.had_error)

    prettyprinter = AstPrinter()
    check.equal(prettyprinter.dump(expr), truth_ast)
