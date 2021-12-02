from textwrap import dedent

import pytest_check as check

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.tokens import Token, TokenType

# Base test cases from https://github.com/munificent/craftinginterpreters/blob/master/test/scanning/strings.lox
TEST_SRC = dedent(
    """\
    ""
    "string"
    'string'
    "multi-
    line-
    string"
    """
)

TRUTH_TOKENS = [
    Token(
        token_type=TokenType.STRING,
        lexeme='""',
        literal="",
        lineno=0,
        end_lineno=0,
        col_offset=0,
        end_col_offset=2,
    ),
    Token(
        token_type=TokenType.STRING,
        lexeme='"string"',
        literal="string",
        lineno=1,
        end_lineno=1,
        col_offset=0,
        end_col_offset=8,
    ),
    Token(
        token_type=TokenType.STRING,
        lexeme="'string'",
        literal="string",
        lineno=2,
        end_lineno=2,
        col_offset=0,
        end_col_offset=8,
    ),
    Token(
        token_type=TokenType.STRING,
        lexeme='"multi-\nline-\nstring"',
        literal="multi-\nline-\nstring",
        lineno=3,
        end_lineno=5,
        col_offset=0,
        end_col_offset=7,
    ),
    Token(
        token_type=TokenType.EOF,
        lexeme="",
        literal=None,
        lineno=6,
        end_lineno=6,
        col_offset=0,
        end_col_offset=0,
    ),
]


def test_string_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
