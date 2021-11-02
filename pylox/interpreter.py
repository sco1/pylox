import typing as t

from pylox import grammar
from pylox.error import LoxRuntimeError
from pylox.protocols import InterpreterProtocol
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
    if obj is None:
        return "nil"

    return str(obj)


class Interpreter:
    def __init__(self, interp: InterpreterProtocol) -> None:
        self._interp = interp  # Terrible name but we're in interpreter.py's Interpreter class v0v

    def interpret(self, expr: grammar.Expr) -> t.Union[str, t.Any]:
        try:
            val = self._evaluate(expr)
            for_print = stringify(val)

            return for_print, val
        except LoxRuntimeError:
            raise NotImplementedError

    def _check_float_operands(self, operator: Token, *operands: t.Any) -> None:
        """Check that the provided operands are all float, generate a runtime error if not."""
        if all((isinstance(operand, float) for operand in operands)):
            return

        self._interp.report_error(LoxRuntimeError(operator, "Operands must be numbers."))

    def _evaluate(self, expr: grammar.Expr) -> t.Any:
        return expr.accept(self)

    def visit_Literal(self, expr: grammar.Literal) -> LITERAL_T:
        return expr.object_value

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
                return float(left) / float(right)
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

            # These diverge from the text since we don't need to handle None like Java handles nil
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right
