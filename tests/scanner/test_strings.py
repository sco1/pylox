from textwrap import dedent

import pytest_check as check

from pylox.scanner import Scanner
from pylox.token import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/strings.lox
TEST_SRC = dedent(
    """\
    ""
    "string"
    'string'

    // expect: STRING ""
    // expect: STRING "string" string
    // expect: STRING 'string' string
    // expect: EOF null
    """
)

TRUTH_TOKENS = [
    Token(token_type=TokenType.STRING, lexeme='""', literal="", lineno=0, col_offset=0),
    Token(token_type=TokenType.STRING, lexeme='"string"', literal="string", lineno=1, col_offset=0),
    Token(token_type=TokenType.STRING, lexeme="'string'", literal="string", lineno=2, col_offset=0),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=8, col_offset=0),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC)
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
