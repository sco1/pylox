from textwrap import dedent

import pytest_check as check

from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/keywords.lox
TEST_SRC = dedent(
    """\
    and class else false for fun if nil or print return super this true var while

    // expect: AND and null
    // expect: CLASS class null
    // expect: ELSE else null
    // expect: FALSE false null
    // expect: FOR for null
    // expect: FUN fun null
    // expect: IF if null
    // expect: NIL nil null
    // expect: OR or null
    // expect: PRINT print null
    // expect: RETURN return null
    // expect: SUPER super null
    // expect: THIS this null
    // expect: TRUE true null
    // expect: VAR var null
    // expect: WHILE while null
    // expect: EOF null
    """
)

TRUTH_TOKENS = [
    Token(token_type=TokenType.AND, lexeme="and", literal=None, lineno=0, col_offset=0),
    Token(token_type=TokenType.CLASS, lexeme="class", literal=None, lineno=0, col_offset=4),
    Token(token_type=TokenType.ELSE, lexeme="else", literal=None, lineno=0, col_offset=10),
    Token(token_type=TokenType.FALSE, lexeme="false", literal=None, lineno=0, col_offset=15),
    Token(token_type=TokenType.FOR, lexeme="for", literal=None, lineno=0, col_offset=21),
    Token(token_type=TokenType.FUN, lexeme="fun", literal=None, lineno=0, col_offset=25),
    Token(token_type=TokenType.IF, lexeme="if", literal=None, lineno=0, col_offset=29),
    Token(token_type=TokenType.NIL, lexeme="nil", literal=None, lineno=0, col_offset=32),
    Token(token_type=TokenType.OR, lexeme="or", literal=None, lineno=0, col_offset=36),
    Token(token_type=TokenType.PRINT, lexeme="print", literal=None, lineno=0, col_offset=39),
    Token(token_type=TokenType.RETURN, lexeme="return", literal=None, lineno=0, col_offset=45),
    Token(token_type=TokenType.SUPER, lexeme="super", literal=None, lineno=0, col_offset=52),
    Token(token_type=TokenType.THIS, lexeme="this", literal=None, lineno=0, col_offset=58),
    Token(token_type=TokenType.TRUE, lexeme="true", literal=None, lineno=0, col_offset=63),
    Token(token_type=TokenType.VAR, lexeme="var", literal=None, lineno=0, col_offset=68),
    Token(token_type=TokenType.WHILE, lexeme="while", literal=None, lineno=0, col_offset=72),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=19, col_offset=0),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC)
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
