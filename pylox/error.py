import typing as t
from dataclasses import dataclass

from pylox.tokens import Token


@dataclass(slots=True)
class LoxException(BaseException):
    """Base Lox exception type."""

    line: int
    col: int
    message: str

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.message}"


class LoxPreProcessorError(LoxException): ...  # noqa: E701


class LoxSyntaxError(LoxException): ...  # noqa: E701


class LoxParseError(LoxException):
    def __init__(self, token: Token, message: str) -> None:
        self.line = token.lineno
        self.col = token.col_offset
        self.message = message


class LoxResolverError(LoxException):
    def __init__(self, token: Token, message: str) -> None:
        self.line = token.lineno
        self.col = token.col_offset
        self.message = message


class LoxRuntimeError(LoxException):
    def __init__(self, token: Token, message: str) -> None:
        self.line = token.lineno
        self.col = token.col_offset
        self.message = message


class LoxReturnError(LoxRuntimeError):
    def __init__(self, value: t.Any) -> None:
        self.value = value


class LoxBreakError(LoxRuntimeError):
    def __init__(self) -> None: ...


class LoxContinueError(LoxRuntimeError):
    def __init__(self) -> None: ...
