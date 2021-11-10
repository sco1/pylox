import time
import typing as t

from pylox.callable import LoxCallable
from pylox.environment import Environment
from pylox.protocols import InterpreterProtocol
from pylox.tokens import Token, TokenType


class Clock(LoxCallable):
    @property
    def arity(self) -> int:
        return 0

    def call(self, interpreter: InterpreterProtocol, arguments: list[t.Any]) -> float:
        return time.time()


BUILTIN_MAPPING = {
    "clock": Clock(),
}


def load_builtins(global_environment: Environment) -> Environment:
    for name, func in BUILTIN_MAPPING.items():
        token = Token(TokenType.FUN, name, None, -1, -1)
        global_environment.define(token, func)

    return global_environment
