from textwrap import dedent

import pytest_check as check

from pylox.scanner import Scanner
from pylox.token import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/identifiers.lox
TEST_SRC = dedent(
    """\
    andy formless fo _ _123 _abc ab123
    abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_

    // expect: IDENTIFIER andy null
    // expect: IDENTIFIER formless null
    // expect: IDENTIFIER fo null
    // expect: IDENTIFIER _ null
    // expect: IDENTIFIER _123 null
    // expect: IDENTIFIER _abc null
    // expect: IDENTIFIER ab123 null
    // expect: IDENTIFIER abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_ null
    // expect: EOF  null
    """
)

TRUTH_TOKENS = [
    Token(token_type=TokenType.IDENTIFIER, lexeme="andy", literal=None, lineno=0, col_offset=0),
    Token(token_type=TokenType.IDENTIFIER, lexeme="formless", literal=None, lineno=0, col_offset=5),
    Token(token_type=TokenType.IDENTIFIER, lexeme="fo", literal=None, lineno=0, col_offset=14),
    Token(token_type=TokenType.IDENTIFIER, lexeme="_", literal=None, lineno=0, col_offset=17),
    Token(token_type=TokenType.IDENTIFIER, lexeme="_123", literal=None, lineno=0, col_offset=19),
    Token(token_type=TokenType.IDENTIFIER, lexeme="_abc", literal=None, lineno=0, col_offset=24),
    Token(token_type=TokenType.IDENTIFIER, lexeme="ab123", literal=None, lineno=0, col_offset=29),
    Token(
        token_type=TokenType.IDENTIFIER,
        lexeme="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_",
        literal=None,
        lineno=1,
        col_offset=0,
    ),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=12, col_offset=0),
]


def test_identifier_scanning() -> None:
    scanner = Scanner(TEST_SRC)
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
