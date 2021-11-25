from functools import partial
from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/punctuators.lox
TEST_SRC = dedent(
    """\
    (){};,+-=!*==<=>=!=<>/.

    // expect: LEFT_PAREN ( null
    // expect: RIGHT_PAREN ) null
    // expect: LEFT_BRACE { null
    // expect: RIGHT_BRACE } null
    // expect: SEMICOLON ; null
    // expect: COMMA , null
    // expect: PLUS + null
    // expect: MINUS - null
    // expect: BANG ! null
    // expect: EQUAL = null
    // expect: STAR * null
    // expect: EQUAL_EQUAL == null
    // expect: LESS_EQUAL <= null
    // expect: GREATER_EQUAL >= null
    // expect: BANG_EQUAL != null
    // expect: LESS < null
    // expect: GREATER > null
    // expect: SLASH / null
    // expect: DOT . null
    // expect: EOF  null
    """
)

PARTIAL_TOKEN = partial(Token, lineno=0, end_lineno=0)

TRUTH_TOKENS = [
    PARTIAL_TOKEN(token_type=TokenType.LEFT_PAREN, lexeme="(", col_offset=0, end_col_offset=1),
    PARTIAL_TOKEN(token_type=TokenType.RIGHT_PAREN, lexeme=")", col_offset=1, end_col_offset=2),
    PARTIAL_TOKEN(token_type=TokenType.LEFT_BRACE, lexeme="{", col_offset=2, end_col_offset=3),
    PARTIAL_TOKEN(token_type=TokenType.RIGHT_BRACE, lexeme="}", col_offset=3, end_col_offset=4),
    PARTIAL_TOKEN(token_type=TokenType.SEMICOLON, lexeme=";", col_offset=4, end_col_offset=5),
    PARTIAL_TOKEN(token_type=TokenType.COMMA, lexeme=",", col_offset=5, end_col_offset=6),
    PARTIAL_TOKEN(token_type=TokenType.PLUS, lexeme="+", col_offset=6, end_col_offset=7),
    PARTIAL_TOKEN(token_type=TokenType.MINUS, lexeme="-", col_offset=7, end_col_offset=8),
    PARTIAL_TOKEN(token_type=TokenType.EQUAL, lexeme="=", col_offset=8, end_col_offset=9),
    PARTIAL_TOKEN(token_type=TokenType.BANG, lexeme="!", col_offset=9, end_col_offset=10),
    PARTIAL_TOKEN(token_type=TokenType.STAR, lexeme="*", col_offset=10, end_col_offset=11),
    PARTIAL_TOKEN(token_type=TokenType.EQUAL_EQUAL, lexeme="==", col_offset=11, end_col_offset=13),
    PARTIAL_TOKEN(token_type=TokenType.LESS_EQUAL, lexeme="<=", col_offset=13, end_col_offset=15),
    PARTIAL_TOKEN(
        token_type=TokenType.GREATER_EQUAL, lexeme=">=", col_offset=15, end_col_offset=17
    ),
    PARTIAL_TOKEN(token_type=TokenType.BANG_EQUAL, lexeme="!=", col_offset=17, end_col_offset=19),
    PARTIAL_TOKEN(token_type=TokenType.LESS, lexeme="<", col_offset=19, end_col_offset=20),
    PARTIAL_TOKEN(token_type=TokenType.GREATER, lexeme=">", col_offset=20, end_col_offset=21),
    PARTIAL_TOKEN(token_type=TokenType.SLASH, lexeme="/", col_offset=21, end_col_offset=22),
    PARTIAL_TOKEN(token_type=TokenType.DOT, lexeme=".", col_offset=22, end_col_offset=23),
    PARTIAL_TOKEN(
        token_type=TokenType.EOF,
        lexeme="",
        lineno=22,
        end_lineno=22,
        col_offset=0,
        end_col_offset=0,
    ),
]


def test_punctuator_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
