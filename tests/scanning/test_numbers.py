from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/numbers.lox
TEST_SRC = dedent(
    """\
    123
    123.456
    .456
    123.

    // expect: NUMBER 123 123
    // expect: NUMBER 123.456 123.456
    // expect: DOT . null
    // expect: NUMBER 456 456
    // expect: NUMBER 123 123
    // expect: DOT . null
    // expect: EOF  null
    """
)

TRUTH_TOKENS = [
    Token(token_type=TokenType.NUMBER, lexeme="123", literal=123, lineno=0, col_offset=0),
    Token(token_type=TokenType.NUMBER, lexeme="123.456", literal=123.456, lineno=1, col_offset=0),
    Token(token_type=TokenType.DOT, lexeme=".", literal=None, lineno=2, col_offset=0),
    Token(token_type=TokenType.NUMBER, lexeme="456", literal=456, lineno=2, col_offset=1),
    Token(token_type=TokenType.NUMBER, lexeme="123", literal=123, lineno=3, col_offset=0),
    Token(token_type=TokenType.DOT, lexeme=".", literal=None, lineno=3, col_offset=3),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=12, col_offset=0),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        # Check literals separately so we can use approximate comparisons on the floats
        truth = TRUTH_TOKENS[idx]
        check.equal(
            (token.token_type, token.lexeme, token.lineno, token.col_offset),
            (truth.token_type, truth.lexeme, truth.lineno, truth.col_offset),
        )
        check.almost_equal(token.literal, truth.literal)
