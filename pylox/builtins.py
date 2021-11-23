import math
import time
import typing as t

from pylox.callable import LoxCallable
from pylox.environment import Environment
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token, TokenType


class BuiltinFunction(LoxCallable):
    """Base class for Lox's built-in functions."""

    def __str__(self) -> str:
        return f"<builtin fn {self._shortname}>"


class Abs(BuiltinFunction):
    _shortname = "abs"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the absolute value of a number."""
        return abs(arguments[0])


class Ceil(BuiltinFunction):
    _shortname = "ceil"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the smallest number greater than or equal to the input value."""
        return math.ceil(arguments[0])


class Clock(BuiltinFunction):
    _shortname = "clock"

    @property
    def arity(self) -> int:  # noqa: D102
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the time in seconds since the epoch as a floating point number."""
        return time.time()


class Floor(BuiltinFunction):
    _shortname = "floor"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the smallest number less than or equal to the input value."""
        return math.floor(arguments[0])


class Max(BuiltinFunction):
    _shortname = "max"

    @property
    def arity(self) -> int:  # noqa: D102
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the maximum of the two values."""
        return max(arguments)


class Min(BuiltinFunction):
    _shortname = "min"

    @property
    def arity(self) -> int:  # noqa: D102
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        """Return the minimum of the two values."""
        return min(arguments)


BUILTIN_MAPPING = {
    "abs": Abs(),
    "ceil": Ceil(),
    "clock": Clock(),
    "floor": Floor(),
    "max": Max(),
    "min": Min(),
}


def load_builtins(global_environment: Environment) -> Environment:
    """Insert Lox's built-ins into the provided global environment."""
    for name, func in BUILTIN_MAPPING.items():
        token = Token(TokenType.FUN, name, None, -1, -1)
        global_environment.define(token, func)

    return global_environment
