from __future__ import annotations

import typing as t

from pylox import grammar


class InterpreterProtocol(t.Protocol):  # pragma: no cover
    def report_error(self) -> None:
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
