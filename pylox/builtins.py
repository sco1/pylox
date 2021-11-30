import math
import statistics
import time
import typing as t
from collections import deque
from pathlib import Path

from pylox.callable import LoxCallable, LoxInstance
from pylox.containers.array import LoxArray
from pylox.environment import Environment
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token, TokenType

NUMERIC = t.Union[float, int]


def _lox_arrayize(in_iter: t.Iterable) -> LoxArray:
    """Build a `LoxArray` instance to represent the input iterable."""
    out_array = LoxArray(0)
    out_array.fields = deque(in_iter)

    return out_array


class BuiltinFunction(LoxCallable):
    """Base class for Lox's built-in functions."""

    def __str__(self) -> str:
        return f"<builtin fn {self._shortname}>"


class Abs(BuiltinFunction):
    _shortname = "abs"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the absolute value of a number."""
        return abs(arguments[0])


class Array(BuiltinFunction):
    _shortname = "array"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[int]) -> LoxArray:
        """Initialize an n-sized Lox array of `None` values."""
        return LoxArray(arguments[0])


class Ceil(BuiltinFunction):
    _shortname = "ceil"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[NUMERIC]) -> int:
        """Return the smallest number greater than or equal to the input value."""
        return math.ceil(arguments[0])


class Clock(BuiltinFunction):
    _shortname = "clock"

    @property
    def arity(self) -> int:  # noqa: D102
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list) -> float:
        """Return the time in seconds since the epoch as a floating point number."""
        return time.time()


class DivMod(BuiltinFunction):
    _shortname = "divmod"

    @property
    def arity(self) -> int:  # noqa: D102
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: NUMERIC) -> LoxArray:
        """Return a `LoxArray` with the quotient and remainder from integer division."""
        return _lox_arrayize(divmod(*arguments))


class Floor(BuiltinFunction):
    _shortname = "floor"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[NUMERIC]) -> int:
        """Return the smallest number less than or equal to the input value."""
        return math.floor(arguments[0])


class Input(BuiltinFunction):
    _shortname = "input"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[str]) -> str:
        """Prompt the user for a line of input using the provided prompt."""
        return input(arguments[0])


class Len(BuiltinFunction):
    _shortname = "len"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> int:
        """
        Return the length of the specified object.

        This assumes that the underlying Python object defines a `__str__` method.
        """
        if isinstance(arguments[0], str):
            return len(arguments[0])

        if isinstance(arguments[0], LoxInstance):
            return len(arguments[0])

        raise NotImplementedError(f"Object of type '{type(arguments[0]).__name__}' has no length.")


class Max(BuiltinFunction):
    _shortname = "max"

    @property
    def arity(self) -> int:  # noqa: D102
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the maximum of the two values."""
        return max(arguments)


class Mean(BuiltinFunction):
    _shortname = "mean"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the sample arithmetic mean of the data in the input `LoxArray`."""
        return statistics.mean(arguments[0].fields)


class Median(BuiltinFunction):
    _shortname = "median"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[LoxArray]) -> float:
        """
        Return the median (middle value) of the input `LoxArray`.

        If the input array contains an even number of data points, the median is interpolated by
        taking the average of the two middle values.
        """
        return statistics.median(arguments[0].fields)


class Min(BuiltinFunction):
    _shortname = "min"

    @property
    def arity(self) -> int:  # noqa: D102
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the minimum of the two values."""
        return min(arguments)


class Mode(BuiltinFunction):
    _shortname = "mode"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the single most common data point from the input `LoxArray`."""
        return statistics.mode(arguments[0].fields)


class Ord(BuiltinFunction):
    _shortname = "ord"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[str]) -> int:
        """Return an integer representing the Unicode code point of the input character."""
        return ord(arguments[0])


class ReadText(BuiltinFunction):
    _shortname = "read_text"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[str]) -> str:
        """Return the contents of the specified file as a string."""
        return Path(arguments[0]).read_text()


class Std(BuiltinFunction):
    _shortname = "std"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the sample standard deviation of the input `LoxArray`."""
        return statistics.stdev(arguments[0].fields)


class StringArray(BuiltinFunction):
    _shortname = "string_array"

    @property
    def arity(self) -> int:  # noqa: D102
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[str]) -> LoxArray:
        """Break the input string into a `LoxArray` of individual characters."""
        return _lox_arrayize(arguments[0])


BUILTIN_MAPPING = {
    "abs": Abs(),
    "array": Array(),
    "ceil": Ceil(),
    "clock": Clock(),
    "divmod": DivMod(),
    "floor": Floor(),
    "input": Input(),
    "len": Len(),
    "max": Max(),
    "mean": Mean(),
    "median": Median(),
    "min": Min(),
    "mode": Mode(),
    "ord": Ord(),
    "read_text": ReadText(),
    "std": Std(),
    "string_array": StringArray(),
}


def load_builtins(global_environment: Environment) -> Environment:
    """Insert Lox's built-ins into the provided global environment."""
    for name, func in BUILTIN_MAPPING.items():
        token = Token(TokenType.FUN, name)
        global_environment.define(token, func)

    return global_environment
