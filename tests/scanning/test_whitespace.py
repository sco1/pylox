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
    Token(
        token_type=TokenType.IDENTIFIER,
        lexeme="space",
        lineno=0,
        end_lineno=0,
        col_offset=0,
        end_col_offset=5,
    ),
    Token(
        token_type=TokenType.IDENTIFIER,
        lexeme="tabs",
        lineno=0,
        end_lineno=0,
        col_offset=9,
        end_col_offset=13,
    ),
    Token(
        token_type=TokenType.IDENTIFIER,
        lexeme="newline",
        lineno=0,
        end_lineno=0,
        col_offset=17,
        end_col_offset=24,
    ),
    Token(
        token_type=TokenType.IDENTIFIER,
        lexeme="end",
        lineno=5,
        end_lineno=5,
        col_offset=0,
        end_col_offset=3,
    ),
    Token(
        token_type=TokenType.EOF,
        lexeme="",
        lineno=12,
        end_lineno=12,
        col_offset=0,
        end_col_offset=0,
    ),
]


def test_whitespace_scanning() -> None:
    scanner = Scanner(TEST_SRC, Lox())
    tokens = scanner.scan_tokens()

    for idx, token in enumerate(tokens):
        check.equal(token, TRUTH_TOKENS[idx])
