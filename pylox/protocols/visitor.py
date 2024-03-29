# THIS FILE HAS BEEN AUTOGENERATED
from __future__ import annotations

import typing as t

from pylox import grammar


class VisitorProtocol(t.Protocol):
    def visit_Assign(self, expr: grammar.Assign) -> t.Any: ...

    def visit_Binary(self, expr: grammar.Binary) -> t.Any: ...

    def visit_Call(self, expr: grammar.Call) -> t.Any: ...

    def visit_Get(self, expr: grammar.Get) -> t.Any: ...

    def visit_Grouping(self, expr: grammar.Grouping) -> t.Any: ...

    def visit_Literal(self, expr: grammar.Literal) -> t.Any: ...

    def visit_Logical(self, expr: grammar.Logical) -> t.Any: ...

    def visit_Set(self, expr: grammar.Set) -> t.Any: ...

    def visit_Super(self, expr: grammar.Super) -> t.Any: ...

    def visit_This(self, expr: grammar.This) -> t.Any: ...

    def visit_Unary(self, expr: grammar.Unary) -> t.Any: ...

    def visit_Variable(self, expr: grammar.Variable) -> t.Any: ...

    def visit_Block(self, expr: grammar.Block) -> t.Any: ...

    def visit_Class(self, expr: grammar.Class) -> t.Any: ...

    def visit_Expression(self, expr: grammar.Expression) -> t.Any: ...

    def visit_Function(self, expr: grammar.Function) -> t.Any: ...

    def visit_If(self, expr: grammar.If) -> t.Any: ...

    def visit_Var(self, expr: grammar.Var) -> t.Any: ...

    def visit_Return(self, expr: grammar.Return) -> t.Any: ...

    def visit_Print(self, expr: grammar.Print) -> t.Any: ...

    def visit_While(self, expr: grammar.While) -> t.Any: ...

    def visit_Break(self, expr: grammar.Break) -> t.Any: ...

    def visit_Continue(self, expr: grammar.Continue) -> t.Any: ...
