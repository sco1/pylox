import typing as t

import rich

from pylox import grammar
from pylox.builtins import load_builtins
from pylox.callable import LoxCallable, LoxClass, LoxFunction, LoxInstance
from pylox.environment import Environment
from pylox.error import LoxBreakError, LoxContinueError, LoxReturnError, LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import LITERAL_T, Token, TokenType


def print(obj: t.Any) -> None:
    """
    Overload `print` with Rich's `print` but also escaping markup tags first.

    Without escaping first, Rich will print e.g. `LoxArray(1)` as an empty string because it
    interprets `[nil]` as a markup tag instead of our array
    """
    rich.print(rich.markup.escape(str(obj)))


def is_truthy(obj: t.Any) -> bool:
    """
    Determine the truthiness of the input object.

    `None` and `False` are falsy, everything else is truthy.
    """
    if obj is None:
        return False

    if isinstance(obj, bool):
        return bool(obj)

    return True


def stringify(obj: t.Any) -> str:
    """
    Return the string representation of the provided object.

    With the exception of `None`, which is special cased to `"nil"`, this just falls back to
    Python's string representation.
    """
    if obj is None:
        return "nil"

    return str(obj)


def _lox_eq(left: t.Any, right: t.Any) -> bool:
    """
    Special case equality since Lox diverges from Python's behavior.

    Two basic assumptions are enforced:
        * `None` (`"nil"`) and `False` are falsy, everything else is truthy
        * Comparison between unlike types is always `False`
        * `nan` (`float("nan")`) is not equal to anything
    """
    # Short circuit on unlike types
    # Since we only have a few data types, a straight type comparison should be fine
    if type(left) is not type(right):
        return False

    return left == right


class Interpreter:
    """The Pylox interpreter!"""

    def __init__(self, interp: InterpreterProtocol) -> None:
        self._interp = interp  # Terrible name but we're in interpreter.py's Interpreter class v0v

        # Environment changes as we change scopes, so we want to keep globals separate
        self.globals = load_builtins(Environment())
        self._environment = self.globals
        self._locals: dict[grammar.Expr, int] = {}

    def interpret(self, statements: list[t.Union[grammar.Expr, grammar.Stmt]]) -> list[t.Any]:
        try:
            retvals = []
            for statement in statements:
                retvals = self._evaluate(statement)

            # Optionally return to help with testing
            return retvals
        except LoxRuntimeError as err:
            self._interp.report_runtime_error(err)

    def resolve(self, expr: grammar.Expr, depth: int) -> None:
        self._locals[expr] = depth

    def _check_numeric_operands(self, operator: Token, *operands: t.Any) -> None:
        """Check that the provided operands are all numeric, generate a runtime error if not."""
        # Need to write the explicit loop (vs `all(isinstance(...))`) since bool subclasses int
        for operand in operands:
            if isinstance(operand, (bool, str)):
                break

            if isinstance(operand, (float, int)):  # pragma: no branch
                continue
        else:
            return

        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def _evaluate(self, expr: t.Union[grammar.Expr, grammar.Stmt]) -> t.Any:
        return expr.accept(self)

    def _execute_block(self, statements: list[grammar.Stmt], environment: Environment) -> None:
        env_cache = self._environment  # Cache this so we can restore when we're done
        try:
            self._environment = environment
            for statement in statements:
                self._evaluate(statement)
        finally:
            self._environment = env_cache

    def _lookup_var(self, name: Token, expr: grammar.Expr) -> t.Any:
        distance = self._locals.get(expr, None)
        if distance is not None:
            return self._environment.get_at(distance, name)
        else:
            return self.globals.get(name)

    def visit_Block(self, stmt: grammar.Block) -> None:
        # Environment scoping will be properly walked by the called method
        self._execute_block(stmt.statements, Environment(self._environment))

    def visit_Class(self, stmt: grammar.Class) -> None:
        superclass = None
        if stmt.superclass is not None:
            superclass = self._evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise LoxRuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self._environment.define(stmt.name, None)

        # Store a reference to the superclass so the methods capture the correct environment as
        # their closure
        if stmt.superclass is not None:
            self._environment = Environment(self._environment)
            self._environment.define(Token(TokenType.SUPER, "super", None, 0, 0), superclass)

        methods = {
            method.name.lexeme: LoxFunction(
                method, self._environment, is_initializer=(method.name.lexeme == "init")
            )
            for method in stmt.methods
        }
        new_class = LoxClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            # Pop the environment so we get back to the current class definition
            self._environment = self._environment.enclosing

        self._environment.assign(stmt.name, new_class)

    def visit_Expression(self, stmt: grammar.Expression) -> None:
        self._evaluate(stmt.expr_expression)

    def visit_Function(self, stmt: grammar.Function) -> None:
        function = LoxFunction(stmt, self._environment)
        self._environment.define(stmt.name, function)

    def visit_If(self, stmt: grammar.If) -> None:
        if is_truthy(self._evaluate(stmt.condition)):
            self._evaluate(stmt.then_branch)
        else:
            if stmt.else_branch is not None:
                self._evaluate(stmt.else_branch)

    def visit_Var(self, stmt: grammar.Var) -> None:
        if stmt.initializer:
            value = self._evaluate(stmt.initializer)
        else:
            value = None

        self._environment.define(stmt.name, value)

    def visit_Print(self, stmt: grammar.Print) -> None:
        value = self._evaluate(stmt.expr_expression)
        print(stringify(value))

    def visit_Return(self, stmt: grammar.Return) -> None:
        value = None
        if stmt.value is not None:
            value = self._evaluate(stmt.value)

        raise LoxReturnError(value)

    def visit_While(self, stmt: grammar.While) -> None:
        try:
            while is_truthy(self._evaluate(stmt.condition)):
                self._evaluate(stmt.body)
        except LoxBreakError:
            return

    def visit_Break(self, stmt: grammar.Break) -> None:
        raise LoxBreakError()

    def visit_Continue(self, stmt: grammar.Continue) -> None:
        raise LoxContinueError()

    def visit_Literal(self, expr: grammar.Literal) -> LITERAL_T:
        return expr.object_value

    def visit_Logical(self, expr: grammar.Logical) -> grammar.Expr:
        left = self._evaluate(expr.expr_left)
        if expr.token_operator.token_type == TokenType.OR:
            # Attempt to short circuit
            if is_truthy(left):
                return left
        else:
            if not is_truthy(left):
                return left

        return self._evaluate(expr.expr_right)

    def visit_Grouping(self, expr: grammar.Grouping) -> t.Any:
        return self._evaluate(expr.expr_expression)

    def visit_Unary(self, expr: grammar.Unary) -> t.Union[float, bool]:
        right = self._evaluate(expr.expr_right)
        match expr.token_operator.token_type:
            case TokenType.MINUS:
                self._check_numeric_operands(expr.token_operator, right)
                return -right
            case TokenType.BANG:
                return not is_truthy(right)
            case _:  # pragma: no cover
                raise LoxRuntimeError(
                    expr, f"Unexpected Unary operator: '{expr.token_operator.lexeme}'"
                )

    def visit_Variable(self, expr: grammar.Variable) -> t.Any:
        return self._lookup_var(expr.name, expr)

    def visit_Assign(self, expr: grammar.Assign) -> t.Any:
        value = self._evaluate(expr.value)

        distance = self._locals.get(expr, None)
        if distance is not None:
            self._environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)

        return value

    def visit_Binary(self, expr: grammar.Binary) -> t.Union[float, str, None]:
        # Unless otherwise stated, left/right expressions are supposed to end up as numbers
        left = self._evaluate(expr.expr_left)
        right = self._evaluate(expr.expr_right)

        match expr.token_operator.token_type:
            case TokenType.MINUS:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left - right
            case TokenType.PLUS:
                # Plus can support both the artithmetic operation as well as string concatenation
                if isinstance(left, bool) or isinstance(right, bool):
                    # Explicitly skip bool since it's an int subclass
                    pass
                elif isinstance(left, (float, int)) and isinstance(right, (float, int)):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return f"{left}{right}"

                raise LoxRuntimeError(
                    expr.token_operator, "Operands must either be both numbers or both strings."
                )
            case TokenType.STAR:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left * right
            case TokenType.SLASH:
                self._check_numeric_operands(expr.token_operator, left, right)
                try:
                    return left / right
                except ZeroDivisionError:
                    return float("nan")
            case TokenType.BACK_SLASH:
                self._check_numeric_operands(expr.token_operator, left, right)
                try:
                    return left // right
                except ZeroDivisionError:
                    return float("nan")
            case TokenType.PERCENT:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left % right
            case TokenType.GREATER:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left >= right
            case TokenType.LESS:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left <= right
            case TokenType.CARAT:
                self._check_numeric_operands(expr.token_operator, left, right)
                return left ** right
            case TokenType.BANG_EQUAL:
                return not _lox_eq(left, right)
            case TokenType.EQUAL_EQUAL:
                return _lox_eq(left, right)
            case _:  # pragma: no cover
                raise LoxRuntimeError(
                    expr, f"Unexpected Binary operator: '{expr.token_operator.lexeme}'"
                )

    def visit_Call(self, expr: grammar.Call) -> None:
        function = self._evaluate(expr.callee)
        arguments = [self._evaluate(argument) for argument in expr.arguments]

        if not isinstance(function, LoxCallable):
            raise LoxRuntimeError(expr.closing_paren, "Can only call functions and classes.")

        if len(arguments) != function.arity:
            raise LoxRuntimeError(
                expr.closing_paren, f"Expected {function.arity} arguments but got {len(arguments)}."
            )

        try:
            return function.call(self, arguments)
        except (NotImplementedError, TypeError) as err:
            raise LoxRuntimeError(expr.closing_paren, str(err))

    def visit_Get(self, expr: grammar.Get) -> None:
        object_ = self._evaluate(expr.object_)
        if isinstance(object_, LoxInstance):
            return object_.get(expr.name)

        raise LoxRuntimeError(expr.name, "Only instances have properties.")

    def visit_Set(self, expr: grammar.Set) -> t.Any:
        object_ = self._evaluate(expr.object_)
        if not isinstance(object_, LoxInstance):
            raise LoxRuntimeError(expr.name, "Only instances have fields.")

        value = self._evaluate(expr.value)
        object_.set(expr.name, value)

        return value

    def visit_Super(self, expr: grammar.Super) -> LoxFunction:
        distance = self._locals[expr]
        superclass: LoxClass = self._environment.get_at(distance, "super")

        # The environment where "this" is bound is always going to be right inside the environment
        # where "super" is bound
        object_: LoxInstance = self._environment.get_at(distance - 1, "this")
        method = superclass.find_method(expr.method.lexeme)

        if method is None:
            raise LoxRuntimeError(expr.method, f"Undefined property '{expr.method.lexeme}'.")

        return method.bind(object_)

    def visit_This(self, expr: grammar.This) -> t.Any:
        return self._lookup_var(expr.keyword, expr)
