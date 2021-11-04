import typing as t

import attr

from pylox.tokens import Token


@attr.s(slots=True)
class Environment:
    """The pylox variable environment!"""

    values: dict[str, t.Any] = attr.ib(factory=dict)

    def define(self, name: str, value: t.Any) -> None:
        """Define a variable for the provided token."""
        self.values[name] = value

    def assign(self, name: Token, value: t.Any) -> None:
        """
        Update the value for the provided variable token.

        Raises if the variable is not in scope.
        """
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        else:
            raise RuntimeError(f"Undefined variable '{name.lexeme}''.")

    def get(self, name: Token) -> t.Any:
        """
        Retrieve the value for the provided variable token.

        Raises if the variable is not in scope.
        """
        try:
            return self.values[name.lexeme]
        except KeyError:
            raise RuntimeError(f"Undefined variable '{name.lexeme}''.")
