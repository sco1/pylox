import typing as t

from pylox import grammar
from pylox.error import LoxParseError
from pylox.protocols import InterpreterProtocol
from pylox.tokens import Token, TokenType


class ParseException(BaseException):  # noqa: D101
    ...


class Parser:
    """
    The Pylox Recursive Descent Parser!

    See `grammar.md` in the project root for the formal grammar definition.
    """

    def __init__(self, tokens: list[Token], interpreter: InterpreterProtocol) -> None:
        self.tokens = tokens
        self._interpreter = interpreter

        self._current = 0

    def parse(self) -> t.Optional[list[t.Union[grammar.Expr, grammar.Stmt]]]:
        """
        Attempt to parse the loaded tokens into a list of statements/expressions.

        All encountered errors will be reported to the interpreter & this method will return `None`.
        """
        statements = []
        while not self._is_eof():
            statements.append(self._declaration())

        return statements

    def _is_eof(self) -> bool:
        """Check if we're at the end of the file & run out of tokens to parse."""
        return self._peek().token_type == TokenType.EOF

    def _advance(self) -> Token:
        """Return the next token to be consumed by the parser & advance the pointer location."""
        if not self._is_eof():
            self._current += 1

        return self._previous()

    def _match(self, *query_token_types: TokenType) -> bool:
        """Check if the current token matches any of the query token type(s)."""
        if any((self._check(query_token) for query_token in query_token_types)):
            self._advance()
            return True

        return False

    def _check(self, query_token_type: TokenType) -> bool:
        """Check if the current token matches the query token type."""
        if self._is_eof():
            return False

        return self._peek().token_type == query_token_type

    def _peek(self) -> Token:
        """Return the current token we have yet to consume."""
        return self.tokens[self._current]

    def _previous(self) -> Token:
        """Return the most recently consumed token."""
        return self.tokens[self._current - 1]

    def _consume(self, query_token_type: TokenType, msg: str) -> t.Union[Token, ParseException]:
        """
        Check if the current token matches the query token type.

        If the current token is a match, the token is consumed & retured. Otherwise, an error is
        raised with the provided error message & a `ParseException` returned to assist with
        synchronization.
        """
        if self._check(query_token_type):
            return self._advance()

        self._report_error(LoxParseError(self._peek(), msg))

    def _report_error(self, err: LoxParseError) -> ParseException:
        """Report the provided error to the invoking interpreter & return an exception for sync."""
        self._interpreter.report_error(err)

        raise ParseException

    def _synchronize(self) -> None:
        """
        Attempt to synchronize the parser back to a stable state.

        If we encounter a parsing error, discard tokens until we've reached a likely statement
        boundary (including EOF).
        """
        self._advance()
        while not self._is_eof():
            if self._previous().token_type == TokenType.SEMICOLON:
                return

            match self._peek().token_type:
                case (
                    TokenType.CLASS
                    | TokenType.FOR
                    | TokenType.FUN
                    | TokenType.IF
                    | TokenType.PRINT
                    | TokenType.RETURN
                    | TokenType.VAR
                    | TokenType.WHILE
                ):
                    return

            self._advance()

    def _declaration(self) -> t.Any:
        """
        Parse the declaration grammar.

        `declaration: varDecl | statement`
        """
        try:
            if self._match(TokenType.VAR):
                return self._variable_declaration()

            return self._statement()
        except ParseException:
            self._synchronize()
            return

    def _variable_declaration(self) -> t.Any:
        """
        Parse the variable declaration grammar.

        `varDecl: "var" IDENTIFIER ( "=" expression )? ";"`
        """
        name = self._consume(TokenType.IDENTIFIER, "Expected variable name.")

        if self._match(TokenType.EQUAL):
            initializer = self._expression()
        else:
            initializer = None

        self._consume(TokenType.SEMICOLON, "Expected ';' after value.")
        return grammar.Var(name, initializer)

    def _statement(self) -> grammar.Stmt:
        """
        Parse the statement grammar.

        `statement: exprStmt | forStmt | ifStmt | printStmt | whileStmt | block`
        """
        if self._match(TokenType.FOR):
            return self._for_statement()

        if self._match(TokenType.IF):
            return self._if_statement()

        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._match(TokenType.WHILE):
            return self._while_statement()

        if self._match(TokenType.LEFT_BRACE):
            return grammar.Block(self._block())

        return self._expression_statement()

    def _for_statement(self) -> grammar.Stmt:
        """
        Parse the for grammar.

        `forStmt: "for" "(" ( varDecl | exprStamt | ";" ) expression? ";" expression? ")" statement`

        Rather than define a new grammar construct, the `for` statement is treated as syntatic sugar
        for `while`, and its body used to generate the equivalent `while` loop.
        """
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'for'.")

        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._variable_declaration()
        else:
            initializer = self._expression_statement()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after loop condition.")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after for clauses.")

        # Build the corresponding while loop block
        body = self._statement()
        if increment is not None:
            body = grammar.Block([body, grammar.Expression(increment)])

        # Treat null condition as infinite loop (i.e. "while true")
        if condition is None:
            condition = grammar.Literal(True)
        body = grammar.While(condition, body)

        if initializer is not None:
            body = grammar.Block([initializer, body])

        return body

    def _if_statement(self) -> grammar.If:
        """
        Parse the if grammar.

        `"if" "(" expression ")" statement ( "else" statement )?`

        The dangling else problem is avoided by binding the `else` statement to the nearest `if`
        statement that precedes it.
        """
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after if condition.")

        then_branch = self._statement()
        if self._match(TokenType.ELSE):
            else_branch = self._statement()
        else:
            else_branch = None

        return grammar.If(condition, then_branch, else_branch)

    def _print_statement(self) -> grammar.Print:
        """
        Parse the print grammar.

        `printStmt: "print" expression ";"`
        """
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return grammar.Print(value)

    def _while_statement(self) -> grammar.While:
        """
        Parse the while grammar.

        `whileStmt: "while" "(" expression ")" statement`
        """
        self._consume(TokenType.LEFT_PAREN, "Expected '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ')' after condition.")
        body = self._statement()

        return grammar.While(condition, body)

    def _expression_statement(self) -> grammar.Expression:
        """
        Parse the expression grammar.

        `expression: equality`
        """
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return grammar.Expression(expr)

    def _block(self) -> list[grammar.Stmt]:
        """
        Parse the block grammar.

        `block: "{" declaration* "}"`
        """
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_eof():
            statements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        return statements

    def _expression(self) -> grammar.Expr:
        """
        Parse the expression grammar.

        `expression: assignment`
        """
        return self._assignment()

    def _assignment(self) -> grammar.Expr:
        """
        Parse the assignment grammar.

        `assignment: IDENTIFIER = assignment | equality`
        """
        expr = self._or()
        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()
            if isinstance(expr, grammar.Variable):
                name = expr.name
                return grammar.Assign(name, value)

            self._report_error(LoxParseError(equals, "Invalid assignment target."))

        return expr

    def _or(self) -> grammar.Expr:
        """
        Parse the logic_or grammar.

        `logic_or: logic_and ( "or" logic_and )*`
        """
        expr = self._and()
        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._and()
            expr = grammar.Logical(expr, operator, right)

        return expr

    def _and(self) -> grammar.Expr:
        """
        Parse the logic_and grammar.

        `logic_and: equality ( "and" equality )*`
        """
        expr = self._equality()
        while self._match(TokenType.AND):
            operator = self._previous()
            right = self._equality()
            expr = grammar.Logical(expr, operator, right)

        return expr

    def _equality(self) -> grammar.Expr:
        """
        Parse the equality grammar.

        `equality: comparison ( ( "!=" | "==" ) comparison )*`
        """
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()

            expr = grammar.Binary(expr, operator, right)

        return expr

    def _comparison(self) -> grammar.Expr:
        """
        Parse the comparison grammar.

        `comparison: term ( ( ">" | ">=" | "<" | "<=" ) term )*`
        """
        expr = self._term()
        while self._match(
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
        ):
            operator = self._previous()
            right = self._term()

            expr = grammar.Binary(expr, operator, right)

        return expr

    def _term(self) -> grammar.Expr:
        """
        Parse the term grammar.

        `term: factor ( ( "-" | "+" ) factor )*`
        """
        expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self._factor()

            expr = grammar.Binary(expr, operator, right)

        return expr

    def _factor(self) -> grammar.Expr:
        """
        Parse the factor grammar.

        `factor: power ( ( "/" | "*" | "%" ) power )*`
        """
        expr = self._power()
        while self._match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator = self._previous()
            right = self._power()

            expr = grammar.Binary(expr, operator, right)

        return expr

    def _power(self) -> grammar.Expr:
        """
        Parse the power grammar.

        `power: unary ( ( "^" ) unary )*`
        """
        expr = self._unary()
        while self._match(TokenType.CARAT):
            operator = self._previous()
            right = self._unary()

            expr = grammar.Binary(expr, operator, right)

        return expr

    def _unary(self) -> grammar.Expr:
        """
        Parse the unary grammar.

        `unary: ( "!" | "-" ) unary | primary`
        """
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()

            return grammar.Unary(operator, right)

        return self._primary()

    def _primary(self) -> grammar.Expr:
        """
        Parse the primary grammar.

        `primary: NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER`
        """
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return grammar.Literal(self._previous().literal)

        if self._match(TokenType.TRUE):
            return grammar.Literal(True)

        if self._match(TokenType.FALSE):
            return grammar.Literal(False)

        if self._match(TokenType.NIL):
            return grammar.Literal(None)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return grammar.Grouping(expr)

        if self._match(TokenType.IDENTIFIER):
            return grammar.Variable(self._previous())

        self._report_error(LoxParseError(self._peek(), "Expected expression."))
