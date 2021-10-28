from textwrap import dedent

import pytest_check as check

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

TRUTH_TOKENS = [
    Token(token_type=TokenType.LEFT_PAREN, lexeme="(", literal=None, lineno=0, col_offset=0),
    Token(token_type=TokenType.RIGHT_PAREN, lexeme=")", literal=None, lineno=0, col_offset=1),
    Token(token_type=TokenType.LEFT_BRACE, lexeme="{", literal=None, lineno=0, col_offset=2),
    Token(token_type=TokenType.RIGHT_BRACE, lexeme="}", literal=None, lineno=0, col_offset=3),
    Token(token_type=TokenType.SEMICOLON, lexeme=";", literal=None, lineno=0, col_offset=4),
    Token(token_type=TokenType.COMMA, lexeme=",", literal=None, lineno=0, col_offset=5),
    Token(token_type=TokenType.PLUS, lexeme="+", literal=None, lineno=0, col_offset=6),
    Token(token_type=TokenType.MINUS, lexeme="-", literal=None, lineno=0, col_offset=7),
    Token(token_type=TokenType.EQUAL, lexeme="=", literal=None, lineno=0, col_offset=8),
    Token(token_type=TokenType.BANG, lexeme="!", literal=None, lineno=0, col_offset=9),
    Token(token_type=TokenType.STAR, lexeme="*", literal=None, lineno=0, col_offset=10),
    Token(token_type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, lineno=0, col_offset=11),
    Token(token_type=TokenType.LESS_EQUAL, lexeme="<=", literal=None, lineno=0, col_offset=13),
    Token(token_type=TokenType.GREATER_EQUAL, lexeme=">=", literal=None, lineno=0, col_offset=15),
    Token(token_type=TokenType.BANG_EQUAL, lexeme="!=", literal=None, lineno=0, col_offset=17),
    Token(token_type=TokenType.LESS, lexeme="<", literal=None, lineno=0, col_offset=19),
    Token(token_type=TokenType.GREATER, lexeme=">", literal=None, lineno=0, col_offset=20),
    Token(token_type=TokenType.SLASH, lexeme="/", literal=None, lineno=0, col_offset=21),
    Token(token_type=TokenType.DOT, lexeme=".", literal=None, lineno=0, col_offset=22),
    Token(token_type=TokenType.EOF, lexeme="", literal=None, lineno=22, col_offset=0),
]


def test_keyword_scanning() -> None:
    scanner = Scanner(TEST_SRC)
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
