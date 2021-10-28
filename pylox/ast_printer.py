from pylox import grammar


class AstPrinter:
    """The pylox AST prettyprinter!"""

    def _parenthesize(self, name: str, *expressions: grammar.Expr) -> str:
        components = [name]
        for expr in expressions:
            components.append(expr.accept(self))

        out_str = f"({' '.join(components)})"
        return out_str

    def dump(self, expr: grammar.Expr) -> str:
        """Return a formatted dump of the tree in `expr`."""
        return expr.accept(self)  # type: ignore[no-any-return]

    def visit_Binary(self, expr: grammar.Binary) -> str:
        return self._parenthesize(expr.token_operator.lexeme, expr.expr_left, expr.expr_right)

    def visit_Grouping(self, expr: grammar.Grouping) -> str:
        return self._parenthesize("group", expr.expr_expression)

    def visit_Literal(self, expr: grammar.Literal) -> str:
        return str(expr.object_value)

    def visit_Unary(self, expr: grammar.Unary) -> str:
        return self._parenthesize(expr.token_operator.lexeme, expr.expr_right)
