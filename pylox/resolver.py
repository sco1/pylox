import typing as t
from enum import Enum, auto

from pylox import grammar
from pylox.error import LoxResolverError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import Token


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver:
    """
    The Pylox resolver!

    This runs at compile time & maps how many scopes are between the current scope and the scope
    where the variable is defined, allowing for more efficient lookups and providing the capability
    to perform some (limited) sentiment analysis.
    """

    def __init__(self, interpreter: InterpreterProtocol) -> None:
        self._interpreter = interpreter

        # Scope stack is LIFO
        # Each scope is a variable name, bool k,v pairs
        self._scopes: list[dict[str, bool]] = []

        # Track whether or not we're inside a function or not; helps with things like not allowing
        # returns outside of a function
        self._current_func = FunctionType.NONE

    def _begin_scope(self) -> None:
        self._scopes.append({})

    def _end_scope(self) -> None:
        self._scopes.pop()

    def _resolve_one(self, stmt: t.Union[grammar.Stmt, grammar.Expr]) -> None:
        stmt.accept(self)

    def resolve(self, stmt: list[grammar.Stmt]) -> None:
        for statement in stmt:
            self._resolve_one(statement)

    def _resolve_local(self, expr: grammar.Expr, name: Token) -> None:
        """
        Attempt to locate & resolve the nearest scope containing the variable `name`.

        Starting with the innermost scope & working outwards, each scope is checked for the
        specified variable and, if found, passed to the interpreter to resolve. If not found in any
        scope, it's left unresolved and assumed to be global.
        """
        for depth, scope in enumerate(reversed(self._scopes)):
            if name.lexeme in scope:
                self._interpreter.resolve(expr, depth)
                return

    def _resolve_function(self, function: grammar.Function, function_type: FunctionType) -> None:
        enclosing_function_type = self._current_func  # Cache to restore after resolving
        self._current_func = function_type

        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)

        self.resolve(function.body)
        self._end_scope()

        self._current_func = enclosing_function_type

    def _declare(self, name: Token) -> None:
        """Add the variable `name` to the innermost scope & mark it as "not ready yet'."""
        if not self._scopes:
            return

        # Disallow redeclaring a variable within the same scope
        if name.lexeme in self._scopes[-1]:
            self._interpreter._interp.report_error(
                LoxResolverError(name, f"Variable {name.lexeme} already declared in this scope.")
            )
            return

        self._scopes[-1][name.lexeme] = False

    def _define(self, name: Token) -> None:
        """Mark the variable `name` as "available" to the innermost scope."""
        if not self._scopes:
            return

        self._scopes[-1][name.lexeme] = True

    def visit_Block(self, stmt: grammar.Block) -> None:
        """Resolve variables in the provided block statement."""
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    def visit_Var(self, stmt: grammar.Var) -> None:
        """Resolve variables in the provided variable statement."""
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self._resolve_one(stmt.initializer)

        self._define(stmt.name)

    def visit_Variable(self, expr: grammar.Variable) -> None:
        """
        Resolve variables in the provided variable expression.

        Attempting to reference a variable from an outer scope in its local initializer
        (e.g. `var a = a;`) will raise an error at compile time.
        """
        if self._scopes and (self._scopes[-1].get(expr.name.lexeme, None) is False):
            self._interpreter._interp.report_error(
                LoxResolverError(expr.name, "Can't read local variable in its own initializer.")
            )
            return

        self._resolve_local(expr, expr.name)

    def visit_Assign(self, expr: grammar.Assign) -> None:
        self._resolve_one(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_Function(self, stmt: grammar.Function) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_Expression(self, stmt: grammar.Expression) -> None:
        self._resolve_one(stmt.expr_expression)

    def visit_If(self, stmt: grammar.If) -> None:
        self._resolve_one(stmt.condition)
        self._resolve_one(stmt.then_branch)
        if stmt.else_branch:
            self._resolve_one(stmt.else_branch)

    def visit_Print(self, stmt: grammar.Print) -> None:
        self._resolve_one(stmt.expr_expression)

    def visit_Return(self, stmt: grammar.Return) -> None:
        # Short-circuit if we're not inside a function
        if self._current_func == FunctionType.NONE:
            self._interpreter._interp.report_error(
                LoxResolverError(stmt.keyword, "Can't return from top-level code.")
            )
            return

        if stmt.value:
            self._resolve_one(stmt.value)

    def visit_While(self, stmt: grammar.While) -> None:
        self._resolve_one(stmt.condition)
        self._resolve_one(stmt.body)

    def visit_Binary(self, expr: grammar.Binary) -> None:
        self._resolve_one(expr.expr_left)
        self._resolve_one(expr.expr_right)

    def visit_Call(self, expr: grammar.Call) -> None:
        self._resolve_one(expr.callee)
        for argument in expr.arguments:
            self._resolve_one(argument)

    def visit_Grouping(self, expr: grammar.Grouping) -> None:
        self._resolve_one(expr.expr_expression)

    def visit_Literal(self, expr: grammar.Literal) -> None:
        return

    def visit_Logical(self, expr: grammar.Logical) -> None:
        self._resolve_one(expr.expr_left)
        self._resolve_one(expr.expr_right)

    def visit_Unary(self, expr: grammar.Unary) -> None:
        self._resolve_one(expr.expr_right)