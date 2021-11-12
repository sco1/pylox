import typing as t

from rich import print

from pylox import grammar
from pylox.builtins import load_builtins
from pylox.callable import LoxCallable, LoxFunction
from pylox.environment import Environment
from pylox.error import LoxReturnError, LoxRuntimeError
from pylox.protocols.interpreter import InterpreterProtocol
from pylox.tokens import LITERAL_T, Token, TokenType


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

    return (left == right)


class Interpreter:
    """The Pylox interpreter!"""

    def __init__(self, interp: InterpreterProtocol) -> None:
        self._interp = interp  # Terrible name but we're in interpreter.py's Interpreter class v0v

        # Environment changes as we change scopes, so we want to keep globals separate
        self.globals = load_builtins(Environment())
        self._environment = self.globals

    def interpret(self, statements: list[t.Union[grammar.Expr, grammar.Stmt]]) -> list[t.Any]:
        try:
            retvals = []
            for statement in statements:
                retvals = self._evaluate(statement)

            # Optionally return to help with testing
            return retvals
        except LoxRuntimeError as err:
            self._interp.report_runtime_error(err)

    def _check_float_operands(self, operator: Token, *operands: t.Any) -> None:
        """Check that the provided operands are all float, generate a runtime error if not."""
        if all((isinstance(operand, float) for operand in operands)):
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

    def visit_Block(self, stmt: grammar.Block) -> None:
        # Environment scoping will be properly walked by the called method
        self._execute_block(stmt.statements, Environment(self._environment))

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
        while is_truthy(self._evaluate(stmt.condition)):
            self._evaluate(stmt.body)

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
                self._check_float_operands(expr.token_operator, right)
                return -float(right)
            case TokenType.BANG:
                return not is_truthy(right)

    def visit_Variable(self, expr: grammar.Variable) -> t.Any:
        return self._environment.get(expr.name)

    def visit_Assign(self, expr: grammar.Assign) -> t.Any:
        value = self._evaluate(expr.value)
        self._environment.assign(expr.name, value)

        return value

    def visit_Binary(self, expr: grammar.Binary) -> t.Union[float, str, None]:
        # Unless otherwise stated, left/right expressions are supposed to end up as numbers
        left = self._evaluate(expr.expr_left)
        right = self._evaluate(expr.expr_right)

        match expr.token_operator.token_type:
            case TokenType.MINUS:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                # Plus can support both the artithmetic operation as well as string concatenation
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)

                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                self._interp.report_runtime_error(
                    LoxRuntimeError(
                        expr.token_operator,
                        "Operands must either be both numbers or both strings.",
                    )
                )
            case TokenType.SLASH:
                self._check_float_operands(expr.token_operator, left, right)
                try:
                    return float(left) / float(right)
                except ZeroDivisionError:
                    return float('nan')
            case TokenType.STAR:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) <= float(right)
            case TokenType.CARAT:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) ** float(right)
            case TokenType.PERCENT:
                self._check_float_operands(expr.token_operator, left, right)
                return float(left) % float(right)
            case TokenType.BANG_EQUAL:
                return not _lox_eq(left, right)
            case TokenType.EQUAL_EQUAL:
                return _lox_eq(left, right)

    def visit_Call(self, expr: grammar.Call) -> None:
        function = self._evaluate(expr.callee)
        arguments = [self._evaluate(argument) for argument in expr.arguments]

        if not isinstance(function, LoxCallable):
            raise LoxRuntimeError(expr.closing_paren, "Can only call functions and classes.")

        if len(arguments) != function.arity:
            raise LoxRuntimeError(
                expr.closing_paren,
                f"Expected {function.arity} arguments but got {len(arguments)}."
            )

        return function.call(self, arguments)
