import typing as t
from abc import ABC, abstractmethod

import attr

from pylox import grammar
from pylox.protocols import InterpreterProtocol


class LoxCallable(ABC):
    @property
    @abstractmethod
    def arity(self) -> int:
        return NotImplemented

    @abstractmethod
    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        return NotImplemented


@attr.s
class LoxFunction(LoxCallable):
    declaration: grammar.Function = attr.ib()

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        environment = interpreter.globals

        for param, val in zip(self.declaration.params, arguments):
            environment.define(param, val)

        interpreter._execute_block(self.declaration.body, environment)

    @property
    def arity(self) -> int:
        return len(self.declaration.params)

    def __string__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"
