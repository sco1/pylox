from __future__ import annotations

import typing as t

from pylox import grammar
from pylox.environment import Environment
from pylox.error import LoxException, LoxRuntimeError


class InterpreterProtocol(t.Protocol):  # pragma: no cover
    globals: Environment

    def report_error(self, err: LoxException) -> None:
        ...

    def report_runtime_error(self, err: LoxRuntimeError) -> None:
        ...

    def _execute_block(self, statements: list[grammar.Stmt], environment: Environment) -> None:
        ...


class VisitorProtocol(t.Protocol):  # pragma: no cover
    def visit_Binary(self, expr: grammar.Binary) -> t.Any:
        ...

    def visit_Grouping(self, expr: grammar.Grouping) -> t.Any:
        ...

    def visit_Literal(self, expr: grammar.Literal) -> t.Any:
        ...

    def visit_Unary(self, expr: grammar.Unary) -> t.Any:
        ...
