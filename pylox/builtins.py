import time
import typing as t

from pylox.callable import LoxCallable
from pylox.environment import Environment
from pylox.protocols import InterpreterProtocol
from pylox.tokens import Token, TokenType


class BuiltinFunction(LoxCallable):
    """Base class for Lox's built-in functions."""

    def __str__(self) -> str:
        return f"<builtin fn {self._shortname}>"


class Clock(BuiltinFunction):
    _shortname = "clock"

    @property
    def arity(self) -> int:  # noqa: D102
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the time in seconds since the epoch as a floating point number."""
        return time.time()


BUILTIN_MAPPING = {
    "clock": Clock(),
}


def load_builtins(global_environment: Environment) -> Environment:
    """Insert Lox's built-ins into the provided global environment."""
    for name, func in BUILTIN_MAPPING.items():
        token = Token(TokenType.FUN, name, None, -1, -1)
        global_environment.define(token, func)

    return global_environment
