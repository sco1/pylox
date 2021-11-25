from functools import partial
from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

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

PARTIAL_TOKEN = partial(Token, lineno=0, end_lineno=0)

TRUTH_TOKENS = [
    PARTIAL_TOKEN(token_type=TokenType.IDENTIFIER, lexeme="andy", col_offset=0, end_col_offset=4),
    PARTIAL_TOKEN(
        token_type=TokenType.IDENTIFIER, lexeme="formless", col_offset=5, end_col_offset=13
    ),
    PARTIAL_TOKEN(token_type=TokenType.IDENTIFIER, lexeme="fo", col_offset=14, end_col_offset=16),
    PARTIAL_TOKEN(token_type=TokenType.IDENTIFIER, lexeme="_", col_offset=17, end_col_offset=18),
    PARTIAL_TOKEN(token_type=TokenType.IDENTIFIER, lexeme="_123", col_offset=19, end_col_offset=23),
    PARTIAL_TOKEN(token_type=TokenType.IDENTIFIER, lexeme="_abc", col_offset=24, end_col_offset=28),
    PARTIAL_TOKEN(
        token_type=TokenType.IDENTIFIER, lexeme="ab123", col_offset=29, end_col_offset=34
    ),
    PARTIAL_TOKEN(
        token_type=TokenType.IDENTIFIER,
        lexeme="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_",
        literal=None,
        lineno=1,
        end_lineno=1,
        col_offset=0,
        end_col_offset=63,
    ),
    PARTIAL_TOKEN(
        token_type=TokenType.EOF,
        lexeme="",
        lineno=12,
        end_lineno=12,
        col_offset=0,
        end_col_offset=0,
    ),
]


def test_identifier_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
