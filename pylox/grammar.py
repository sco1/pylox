# THIS FILE HAS BEEN AUTOGENERATED
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

import attr

from pylox.tokens import LITERAL_T, Token


class Expr(ABC):  # pragma: no cover
    pass

    @abstractmethod
    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return NotImplemented


@attr.s(slots=True)
class Binary(Expr):
    expr_left: Expr = attr.ib()
    token_operator: Token = attr.ib()
    expr_right: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Binary(self)


@attr.s(slots=True)
class Grouping(Expr):
    expr_expression: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Grouping(self)


@attr.s(slots=True)
class Literal(Expr):
    object_value: LITERAL_T = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Literal(self)


@attr.s(slots=True)
class Unary(Expr):
    token_operator: Token = attr.ib()
    expr_right: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Unary(self)


class VisitorProtocol(t.Protocol):  # pragma: no cover
    def visit_Binary(self, expr: Binary) -> t.Any:
        ...

    def visit_Grouping(self, expr: Grouping) -> t.Any:
        ...

    def visit_Literal(self, expr: Literal) -> t.Any:
        ...

    def visit_Unary(self, expr: Unary) -> t.Any:
        ...
