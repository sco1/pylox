import typing as t
from abc import ABC, abstractmethod

import attr

from pylox import grammar
from pylox.protocols import InterpreterProtocol


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

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        """Call the current function instance using the provided arguments."""
        environment = interpreter.globals

        for param, val in zip(self.declaration.params, arguments):
            environment.define(param, val)

        interpreter._execute_block(self.declaration.body, environment)

    @property
    def arity(self) -> int:  # noqa: D102
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
