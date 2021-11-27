from __future__ import annotations

import typing as t

import attr

from pylox.callable import LoxCallable, LoxInstance
from pylox.error import LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token


@attr.s
class _ContainerSetter(LoxCallable):
    parent: LoxContainer = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 2

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        idx, value = arguments

        try:
            self.parent.fields[idx] = value
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Assignment index out of range.")


@attr.s
class _ContainerGetter(LoxCallable):
    parent: LoxContainer = attr.ib()
    call_token: Token = attr.ib()

    @property
    def arity(self) -> int:
        return 1

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> t.Any:
        try:
            return self.parent.fields[arguments[0]]
        except IndexError:
            raise LoxRuntimeError(self.call_token, "Index out of range.")


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

    def get(self, method_name: Token) -> t.Any:
        """Define basic setting & indexing methods."""
        match method_name.lexeme:
            case "get":
                return _ContainerGetter(self, method_name)
            case "set":
                return _ContainerSetter(self, method_name)
            case _:
                raise LoxRuntimeError(method_name, f"Undefined method: '{method_name.lexeme}'")

    def set(self, val: t.Any) -> None:
        """Block `Set` expression, all methods dispatched by `Get` expressions."""
        raise LoxRuntimeError(val, "Cannot add properties to LoxSet.")
