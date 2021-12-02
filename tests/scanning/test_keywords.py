from functools import partial
from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/keywords.lox
TEST_SRC = dedent(
    """\
    and class else false for fun if nil or print return super this true var while break continue include
    """
)

PARTIAL_TOKEN = partial(Token, lineno=0, end_lineno=0)
TRUTH_TOKENS = [
    PARTIAL_TOKEN(token_type=TokenType.AND, lexeme="and", col_offset=0, end_col_offset=3),
    PARTIAL_TOKEN(token_type=TokenType.CLASS, lexeme="class", col_offset=4, end_col_offset=9),
    PARTIAL_TOKEN(token_type=TokenType.ELSE, lexeme="else", col_offset=10, end_col_offset=14),
    PARTIAL_TOKEN(token_type=TokenType.FALSE, lexeme="false", col_offset=15, end_col_offset=20),
    PARTIAL_TOKEN(token_type=TokenType.FOR, lexeme="for", col_offset=21, end_col_offset=24),
    PARTIAL_TOKEN(token_type=TokenType.FUN, lexeme="fun", col_offset=25, end_col_offset=28),
    PARTIAL_TOKEN(token_type=TokenType.IF, lexeme="if", col_offset=29, end_col_offset=31),
    PARTIAL_TOKEN(token_type=TokenType.NIL, lexeme="nil", col_offset=32, end_col_offset=35),
    PARTIAL_TOKEN(token_type=TokenType.OR, lexeme="or", col_offset=36, end_col_offset=38),
    PARTIAL_TOKEN(token_type=TokenType.PRINT, lexeme="print", col_offset=39, end_col_offset=44),
    PARTIAL_TOKEN(token_type=TokenType.RETURN, lexeme="return", col_offset=45, end_col_offset=51),
    PARTIAL_TOKEN(token_type=TokenType.SUPER, lexeme="super", col_offset=52, end_col_offset=57),
    PARTIAL_TOKEN(token_type=TokenType.THIS, lexeme="this", col_offset=58, end_col_offset=62),
    PARTIAL_TOKEN(token_type=TokenType.TRUE, lexeme="true", col_offset=63, end_col_offset=67),
    PARTIAL_TOKEN(token_type=TokenType.VAR, lexeme="var", col_offset=68, end_col_offset=71),
    PARTIAL_TOKEN(token_type=TokenType.WHILE, lexeme="while", col_offset=72, end_col_offset=77),
    PARTIAL_TOKEN(token_type=TokenType.BREAK, lexeme="break", col_offset=78, end_col_offset=83),
    PARTIAL_TOKEN(
        token_type=TokenType.CONTINUE, lexeme="continue", col_offset=84, end_col_offset=92
    ),
    PARTIAL_TOKEN(
        token_type=TokenType.INCLUDE, lexeme="include", col_offset=93, end_col_offset=100
    ),
    PARTIAL_TOKEN(
        token_type=TokenType.EOF,
        lexeme="",
        lineno=1,
        end_lineno=1,
        col_offset=0,
        end_col_offset=0,
    ),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    print(f"n tokens: {len(tokens)}")

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
