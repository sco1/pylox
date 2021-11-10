# THIS FILE HAS BEEN AUTOGENERATED
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

import attr

from pylox.protocols import VisitorProtocol
from pylox.tokens import LITERAL_T, Token


class Expr(ABC):  # pragma: no cover
    pass

    @abstractmethod
    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return NotImplemented


@attr.s(slots=True)
class Assign(Expr):
    name: Token = attr.ib()
    value: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Assign(self)


@attr.s(slots=True)
class Binary(Expr):
    expr_left: Expr = attr.ib()
    token_operator: Token = attr.ib()
    expr_right: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Binary(self)


@attr.s(slots=True)
class Call(Expr):
    callee: Expr = attr.ib()
    closing_paren: Token = attr.ib()
    arguments: list[Expr] = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Call(self)


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
class Logical(Expr):
    expr_left: Expr = attr.ib()
    token_operator: Token = attr.ib()
    expr_right: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Logical(self)


@attr.s(slots=True)
class Variable(Expr):
    name: Token = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Variable(self)


@attr.s(slots=True)
class Unary(Expr):
    token_operator: Token = attr.ib()
    expr_right: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Unary(self)


class Stmt(ABC):  # pragma: no cover
    pass

    @abstractmethod
    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return NotImplemented


@attr.s(slots=True)
class Block(Stmt):
    statements: list[Stmt] = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Block(self)


@attr.s(slots=True)
class Expression(Stmt):
    expr_expression: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Expression(self)


@attr.s(slots=True)
class Function(Stmt):
    name: Token = attr.ib()
    params: list[Token] = attr.ib()
    body: list[Stmt] = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Function(self)


@attr.s(slots=True)
class If(Stmt):
    condition: Expr = attr.ib()
    then_branch: Stmt = attr.ib()
    else_branch: t.Optional[Stmt] = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_If(self)


@attr.s(slots=True)
class Var(Stmt):
    name: Token = attr.ib()
    initializer: t.Optional[Expr] = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Var(self)


@attr.s(slots=True)
class Print(Stmt):
    expr_expression: Expr = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_Print(self)


@attr.s(slots=True)
class While(Stmt):
    condition: Expr = attr.ib()
    body: Stmt = attr.ib()

    def accept(self, visitor: VisitorProtocol) -> t.Any:
        return visitor.visit_While(self)
