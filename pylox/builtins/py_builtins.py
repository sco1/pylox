import math
import re
import statistics
import time
import typing as t
from collections import deque
from pathlib import Path

from pylox.callable import LoxCallable, LoxInstance
from pylox.containers.array import LoxArray
from pylox.environment import Environment
from pylox.protocols.interpreter import SourceInterpreterProtocol
from pylox.tokens import Token, TokenType

NUMERIC = t.Union[float, int]


def _lox_arrayize(in_iter: t.Iterable) -> LoxArray:
    """Build a `LoxArray` instance to represent the input iterable."""
    out_array = LoxArray(0)
    out_array.fields = deque(in_iter)

    return out_array


def _arrayize_match(in_match: re.Match | None) -> LoxArray:
    """
    Expand the provided match object into a `LoxArray`.

    If the match is not empty, the first element of the resulting array is the full match followed
    by all group matches, if there was grouping in the pattern.
    """
    if in_match:
        return _lox_arrayize((in_match[0], *in_match.groups()))
    else:
        return LoxArray(0)


class BuiltinFunction(LoxCallable):  # pragma: no cover
    """Base class for Lox's built-in functions."""

    _shortname: str

    def __str__(self) -> str:
        return f"<builtin fn {self._shortname}>"


class Abs(BuiltinFunction):
    _shortname = "abs"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the absolute value of a number."""
        return abs(arguments[0])


class Array(BuiltinFunction):
    _shortname = "array"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[int]) -> LoxArray:
        """Initialize an n-sized Lox array of `None` values."""
        return LoxArray(arguments[0])


class Ceil(BuiltinFunction):
    _shortname = "ceil"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> int:
        """Return the smallest number greater than or equal to the input value."""
        return math.ceil(arguments[0])


class Clock(BuiltinFunction):
    _shortname = "clock"

    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list) -> float:
        """Return the time in seconds since the epoch as a floating point number."""
        return time.time()


class DivMod(BuiltinFunction):
    _shortname = "divmod"

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> LoxArray:
        """Return a `LoxArray` with the quotient and remainder from integer division."""
        return _lox_arrayize(divmod(arguments[0], arguments[1]))


class Floor(BuiltinFunction):
    _shortname = "floor"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> int:
        """Return the smallest number less than or equal to the input value."""
        return math.floor(arguments[0])


class Input(BuiltinFunction):
    _shortname = "input"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> str:
        """Prompt the user for a line of input using the provided prompt."""
        return input(arguments[0])


class Len(BuiltinFunction):
    _shortname = "len"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[t.Any]) -> int:
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
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the maximum of the two values."""
        return max(arguments)


class Mean(BuiltinFunction):
    _shortname = "mean"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the sample arithmetic mean of the data in the input `LoxArray`."""
        return statistics.mean(arguments[0].fields)


class Median(BuiltinFunction):
    _shortname = "median"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[LoxArray]) -> float:
        """
        Return the median (middle value) of the input `LoxArray`.

        If the input array contains an even number of data points, the median is interpolated by
        taking the average of the two middle values.
        """
        return statistics.median(arguments[0].fields)


class Min(BuiltinFunction):
    _shortname = "min"

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[NUMERIC]) -> NUMERIC:
        """Return the minimum of the two values."""
        return min(arguments)


class Mode(BuiltinFunction):
    _shortname = "mode"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the single most common data point from the input `LoxArray`."""
        return statistics.mode(arguments[0].fields)


class Ord(BuiltinFunction):
    _shortname = "ord"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> int:
        """Return an integer representing the Unicode code point of the input character."""
        return ord(arguments[0])


class ReFindall(BuiltinFunction):
    _shortname = "re_findall"

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> LoxArray:
        """
        Return all non-overlapping matches of pattern in string, as an array of strings or arrays.

        The string is scanned left-to-right, and matches are returned in the order found. Empty
        matches are included in the result.

        The result depends on the number of capturing groups in the pattern. If there are no groups,
        return an array of strings matching the whole pattern. If there is exactly one group, return
        an array of strings matching that group. If multiple groups are present, return an array of
        arrays of strings matching the groups.

        Non-capturing groups do not affect the form of the result.
        """
        matches = re.findall(arguments[0], arguments[1])
        if isinstance(matches[0], tuple):
            return _lox_arrayize((_lox_arrayize(groups) for groups in matches))
        else:
            return _lox_arrayize(matches)


class ReMatch(BuiltinFunction):
    _shortname = "re_match"

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> LoxArray:
        """
        Match if the pattern matches zero or more characters at the beginning of the string.

        The first value in the array will always correspond to `match.group(0)`; if the pattern
        contains one or more groups then the array will match the output of `match.groups()`
        """
        return _arrayize_match(re.match(arguments[0], arguments[1]))


class ReSearch(BuiltinFunction):
    _shortname = "re_search"

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> LoxArray:
        """
        Scan through string looking for the first location where the pattern produces a match.

        The first value in the array will always correspond to `match.group(0)`; if the pattern
        contains one or more groups then the array will match the output of `match.groups()`
        """
        return _arrayize_match(re.search(arguments[0], arguments[1]))


class ReSub(BuiltinFunction):
    _shortname = "re_sub"

    @property
    def arity(self) -> int:
        return 3

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> str:
        """Replace the leftmost non-overlapping occurrences of the pattern in the given string."""
        return re.sub(arguments[0], arguments[1], arguments[2])


class ReadText(BuiltinFunction):
    _shortname = "read_text"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> str:
        """Return the contents of the specified file as a string."""
        return Path(arguments[0]).read_text()


class Std(BuiltinFunction):
    _shortname = "std"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[LoxArray]) -> float:
        """Return the sample standard deviation of the input `LoxArray`."""
        return statistics.stdev(arguments[0].fields)


class Str2Num(BuiltinFunction):
    _shortname = "str2num"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> NUMERIC:
        """Convert the provided string into an integer or float."""
        try:
            return int(arguments[0])
        except ValueError:
            try:
                return float(arguments[0])
            except ValueError:
                pass

        raise ValueError(f"Cannot convert '{arguments[0]}' to an integer or float.")


class StringArray(BuiltinFunction):
    _shortname = "string_array"

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[str]) -> LoxArray:
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
    "re_findall": ReFindall(),
    "re_match": ReMatch(),
    "re_search": ReSearch(),
    "re_sub": ReSub(),
    "read_text": ReadText(),
    "std": Std(),
    "str2num": Str2Num(),
    "string_array": StringArray(),
}


def load_builtins(global_environment: Environment) -> Environment:
    """Insert Lox's built-ins into the provided global environment."""
    for name, func in BUILTIN_MAPPING.items():
        token = Token(TokenType.FUN, name)
        global_environment.define(token, func)

    return global_environment
