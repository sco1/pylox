from __future__ import annotations

import typing as t
from collections import deque

import attr

from pylox.callable import LoxCallable
from pylox.containers.base import LoxContainer
from pylox.error import LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token


@attr.s
class _Append(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        self.parent.fields.append(arguments[0])


@attr.s
class _AppendLeft(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        self.parent.fields.appendleft(arguments[0])


@attr.s
class _Clear(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        self.parent.fields.clear()


@attr.s
class _Pop(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        try:
            return self.parent.fields.pop()
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Cannot pop from empty array.")


@attr.s
class _PopLeft(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        try:
            return self.parent.fields.popleft()
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Cannot pop from empty array.")


@attr.s
class _Reverse(LoxCallable):
    parent: LoxArray = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        return self.parent.fields.reverse()


class LoxArray(LoxContainer):
    """
    A collection of heterogeneous data types.

    The `LoxArray` supports memory efficient appends and pops from either side of the array with
    approximately the same O(1) performance in either direction. Because it uses Python's `deque`.
    """

    def __init__(self, size: int) -> None:
        self.instance_of = LoxArray
        self.fields = deque([None] * size)

    def __str__(self) -> str:
        """Build a more `list`-like string representation to disguise that we're using `deque`."""
        # Manual loop rather than list comp since we need to explicitly handle None as "nil"
        out_contents = []
        for thing in self.fields:
            if thing is None:
                out_contents.append("nil")
            else:
                out_contents.append(repr(thing))

        return f"[{', '.join(out_contents)}]"

    def get(self, method_name: Token) -> LoxCallable:
        """Dispatch the matching Array method, or raise `LoxRuntimeError` if not defined."""
        try:
            # Check base indexing operations first
            return super().get(method_name)
        except LoxRuntimeError:
            pass

        match method_name.lexeme:
            case "append":
                return _Append(self, method_name)
            case "appendleft":
                return _AppendLeft(self, method_name)
            case "clear":
                return _Clear(self, method_name)
            case "pop":
                return _Pop(self, method_name)
            case "popleft":
                return _PopLeft(self, method_name)
            case "reverse":
                return _Reverse(self, method_name)
            case _:
                raise LoxRuntimeError(method_name, f"Undefined method: '{method_name.lexeme}'.")
