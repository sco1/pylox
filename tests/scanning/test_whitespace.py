from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/whitespace.lox
TEST_SRC = dedent(
    """\
    space    tabs				newline




    end

    // expect: IDENTIFIER space null
    // expect: IDENTIFIER tabs null
    // expect: IDENTIFIER newline null
    // expect: IDENTIFIER end null
    // expect: EOF  null
    """
)

TRUTH_TOKENS = [
    Token(token_type=TokenType.IDENTIFIER, lexeme="space", literal=None, lineno=0, col_offset=0),
    Token(token_type=TokenType.IDENTIFIER, lexeme="tabs", literal=None, lineno=0, col_offset=9),
    Token(token_type=TokenType.IDENTIFIER, lexeme="newline", literal=None, lineno=0, col_offset=17),
    Token(token_type=TokenType.IDENTIFIER, lexeme="end", literal=None, lineno=5, col_offset=0),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=12, col_offset=0),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
