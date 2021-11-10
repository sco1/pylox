from __future__ import annotations

import typing as t

import attr

from pylox.error import LoxRuntimeError
from pylox.tokens import Token


@attr.s(slots=True)
class Environment:
    """The pylox variable environment!"""

    enclosing: t.Optional[Environment] = attr.ib(default=None)
    values: dict[str, t.Any] = attr.ib(factory=dict)

    def define(self, name: Token, value: t.Any) -> None:
        """
        Define a variable for the provided token.

        Raises if we are not in the global scope and a variable of the same name already exists in
        the current scope.
        """
        if self.enclosing and (name.lexeme in self.values):
            raise LoxRuntimeError(name, f"Cannot redefine '{name.lexeme}' in a non-global scope.")

        self.values[name.lexeme] = value

    def assign(self, name: Token, value: t.Any) -> None:
        """
        Update the value for the provided variable token.

        Raises if the variable is not in the current scope or higher.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        else:
            if self.enclosing is not None:
                self.enclosing.assign(name, value)
                return

            raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get(self, name: Token) -> t.Any:
        """
        Retrieve the value for the provided variable token.

        Raises if the variable is not in the current scope or higher.
        """
        try:
            return self.values[name.lexeme]
        except KeyError:
            # If we're in an enclosed scope, walk upwards to see if the variable is defined there
            if self.enclosing is not None:
                return self.enclosing.get(name)
            else:
                raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
