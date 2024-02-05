from __future__ import annotations

import typing as t

from pylox import grammar
from pylox.environment import Environment
from pylox.error import LoxException, LoxRuntimeError


class LoxInterpreterProtocol(t.Protocol):  # pragma: no cover
    def report_error(self, err: LoxException) -> None: ...

    def report_runtime_error(self, err: LoxRuntimeError) -> None: ...


class SourceInterpreterProtocol(t.Protocol):  # pragma: no cover
    globals: Environment
    _interp: LoxInterpreterProtocol

    def _execute_block(self, statements: list[grammar.Stmt], environment: Environment) -> None: ...

    def resolve(self, expr: grammar.Expr, depth: int) -> None: ...
