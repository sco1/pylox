from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

import attr

from pylox import grammar
from pylox.environment import Environment
from pylox.error import LoxReturnError, LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token, TokenType


class LoxCallable(ABC):  # pragma: no cover
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
    is_initializer: bool = attr.ib(default=False)

    def bind(self, instance: LoxInstance) -> SelfLoxFunction:
        """For class methods, define a nested closure with the instance pre-defined as `this`."""
        env = Environment(self.closure)
        env.define(Token(TokenType.THIS, "this", None, 0, 0), instance)
        return LoxFunction(self.declaration, env, self.is_initializer)

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> t.Any:
        """Call the current function instance using the provided arguments."""
        environment = Environment(self.closure)

        for param, val in zip(self.declaration.params, arguments):
            environment.define(param, val)

        try:
            interpreter._execute_block(self.declaration.body, environment)
        except LoxReturnError as func_return:
            # Return current instance if we short-circuit from the class init
            if self.is_initializer:
                return self.closure.get_at(0, "this")

            return func_return.value

        # Class constructor will always return the current instance, even if called directly
        if self.is_initializer:
            return self.closure.get_at(0, "this")

    @property
    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"


SelfLoxClass = t.TypeVar("SelfLoxClass", bound="LoxClass")


@attr.s
class LoxClass(LoxCallable):
    name: str = attr.ib()
    superclass: SelfLoxClass = attr.ib()
    methods: dict = attr.ib()

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> SelfLoxClass:
        instance = LoxInstance(self)

        # Check for an initializer & call it if defined
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    @property
    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        else:
            return initializer.arity

    def find_method(self, name: str) -> t.Optional[LoxFunction]:
        """
        Attempt to find a class method with the provided name.

        If the current class is a subclass, locally defined methods overload a superclass method of
        the same name. If the subclass does not overload the method, the inheritance is followed
        upwards to attempt to locate a method.
        """
        if name in self.methods:
            return self.methods[name]

        if self.superclass is not None:
            return self.superclass.find_method(name)

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
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return f"<inst {self.instance_of.name}>"
