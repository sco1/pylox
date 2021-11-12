import typing as t
from abc import ABC, abstractmethod

import attr

from pylox import grammar
from pylox.environment import Environment
from pylox.error import LoxReturnError
from pylox.protocols.interpreter import InterpreterProtocol


class LoxCallable(ABC):  # noqa: D101
    @property
    @abstractmethod
    def arity(self) -> int:  # noqa: D102
        return NotImplemented

    @abstractmethod
    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:  # noqa: D102
        return NotImplemented


@attr.s
class LoxFunction(LoxCallable):
    """Lox function implementation."""

    declaration: grammar.Function = attr.ib()
    closure: Environment = attr.ib()

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> t.Any:
        """Call the current function instance using the provided arguments."""
        environment = Environment(self.closure)

        for param, val in zip(self.declaration.params, arguments):
            environment.define(param, val)

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except LoxReturnError as func_return:
            return func_return.value

    @property
    def arity(self) -> int:  # noqa: D102
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
