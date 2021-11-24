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

    def _ancestor(self, distance: int) -> Environment:
        """
        Walk the specified distance up the enclosing scope(s) and return the `Environment`.

        This should always be getting called after the resolver is finished, so it's assumed that
        there is a scope at the specified distance.
        """
        env = self
        for _ in range(distance):
            env = env.enclosing

        return env

    def define(self, name: Token, value: t.Any) -> None:
        """
        Define a variable for the provided token.

        Raises if we are not in the global scope and a variable of the same name already exists in
        the current scope.
        """
        self.values[name.lexeme] = value

    def assign(self, name: Token, value: t.Any) -> None:
        """
        Update the value for the provided variable token.

        Raises if the variable is not in the current scope or higher.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, distance: int, name: Token, value: t.Any) -> None:
        """
        Update the value for the provided variable token in the scope at the specified distance.

        This should always be getting called after the resolver is finished, so it's assumed that
        the variable is present in the scope at the specified distance.
        """
        self._ancestor(distance).values[name.lexeme] = value

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

    def get_at(self, distance: int, name: t.Union[Token, str]) -> t.Any:
        """
        Retrieve the value for the provided variable from the scope at the specified distance.

        This should always be getting called after the resolver is finished, so it's assumed that
        the variable is present in the scope at the specified distance.
        """
        if isinstance(name, Token):
            query = name.lexeme
        else:
            query = name

        return self._ancestor(distance).values[query]
