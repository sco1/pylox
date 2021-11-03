import typing as t

import attr

from pylox.tokens import Token


@attr.s(slots=True)
class Environment:
    values: dict[str, t.Any] = attr.ib(factory=dict)

    def define(self, name: str, value: t.Any) -> t.Any:
        self.values[name] = value

    def get(self, name: Token) -> t.Any:
        try:
            self.values[name.lexeme]
        except KeyError:
            raise NotImplementedError
