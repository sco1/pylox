import typing as t
from enum import Enum, auto

import attr

LITERAL_T = t.Union[str, float, bool, None]


class TokenType(Enum):  # noqa: D101
    # One character token
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()  # !
    BANG_EQUAL = auto()  # !=
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Reserved Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FOR = auto()
    FUN = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


@attr.s(slots=True)
class Token:  # noqa: D101
    token_type: TokenType = attr.ib()
    lexeme: str = attr.ib()
    literal: LITERAL_T = attr.ib()
    lineno: int = attr.ib()  # Zero-indexed
    col_offset: int = attr.ib()  # Zero-indexed

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"
