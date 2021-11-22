from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

import attr

from pylox import grammar
from pylox.environment import Environment
from pylox.error import LoxReturnError, LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token, TokenType


class LoxCallable(ABC):
    @property
    @abstractmethod
    def arity(self) -> int:
        return NotImplemented

    @abstractmethod
    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> None:
        return NotImplemented


SelfLoxFunction = t.TypeVar("SelfLoxFunction", bound="LoxFunction")


@attr.s
class LoxFunction(LoxCallable):
    declaration: grammar.Function = attr.ib()
    closure: Environment = attr.ib()

    def bind(self, instance: LoxInstance) -> SelfLoxFunction:
        """For class methods, define a nested closure with the instance pre-defined as `this`."""
        env = Environment(self.closure)
        env.define(Token(TokenType.THIS, "this", None, 0, 0), instance)
        return LoxFunction(self.declaration, env)

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
    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"


SelfLoxClass = t.TypeVar("SelfLoxClass", bound="LoxClass")


@attr.s
class LoxClass(LoxCallable):
    name: str = attr.ib()
    methods: dict = attr.ib()

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> SelfLoxClass:
        instance = LoxInstance(self)
        return instance

    @property
    def arity(self) -> int:
        return 0

    def find_method(self, name: str) -> t.Any:
        return self.methods.get(name, None)

    def __str__(self) -> str:
        return f"<cls {self.name}>"


@attr.s
class LoxInstance:
    instance_of: LoxClass = attr.ib()
    fields: dict = attr.ib(factory=dict)

    def get(self, name: Token) -> t.Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.instance_of.find_method(name.lexeme)
        if method is not None:
            # bind gives the method a closure with the instance pre-defined as "this"
            return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: t.Any) -> None:
        self.fields[name] = value

    def __str__(self) -> str:
        return f"<inst {self.instance_of.name}>"
