from __future__ import annotations

import typing as t
from dataclasses import dataclass

from pylox.callable import LoxCallable, LoxInstance
from pylox.error import LoxRuntimeError
from pylox.protocols.interpreter import SourceInterpreterProtocol
from pylox.tokens import Token


@dataclass
class _ContainerSetter(LoxCallable):
    parent: LoxContainer
    call_token: Token

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[t.Any]) -> None:
        idx, value = arguments

        try:
            self.parent.fields[idx] = value
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Assignment index out of range.") from None


@dataclass
class _ContainerGetter(LoxCallable):
    parent: LoxContainer
    call_token: Token

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: SourceInterpreterProtocol, arguments: list[t.Any]) -> t.Any:
        try:
            return self.parent.fields[arguments[0]]
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Index out of range.") from None


class LoxContainer(LoxInstance):
    """
    Base class for Lox's container types.

    Since we've defined our builtin calls as objects already, we have to get creative with method
    access. Methods are dispatched from the instance's `Get` expression as instances of
    `LoxCallable`. `Set` expressions are blocked by default.
    """

    def __len__(self) -> int:
        return len(self.fields)

    def __str__(self) -> str:
        return str(self.fields)

    def get(self, method_name: Token) -> LoxCallable:
        """Define basic setting & indexing methods."""
        match method_name.lexeme:
            case "get":
                return _ContainerGetter(self, method_name)
            case "set":
                return _ContainerSetter(self, method_name)
            case _:
                raise LoxRuntimeError(method_name, f"Undefined method: '{method_name.lexeme}'")

    def set(self, name: Token, val: t.Any) -> None:
        """Block `Set` expression, all methods dispatched by `Get` expressions."""
        raise LoxRuntimeError(val, "Cannot add properties to LoxSet.")
