from pylox import grammar
from pylox.tokens import Token, TokenType


class Parser:
    """
    The Pylox Recursive Descent Parser!

    See `grammar.md` in the project root for the formal grammar definition.
    """

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

        self._current = 0

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

    def _consume(self, query_token_type: TokenType, msg: str) -> Token:
        """
        Check if the current token matches the query token type.

        If the current token is a match, the token is consumed & retured. Otherwise, an error is
        raised with the provided error message.
        """
        if self._check(query_token_type):
            return self._advance()

        raise NotImplementedError  # Need to set up error handling so we can raise a syntax error

    def _expression(self) -> grammar.Expr:
        """
        Parse the expression grammar.

        `expression: equality`
        """
        return self._equality()

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

        `factor: unary ( ( "/" | "*" ) unary )*`
        """
        expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
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

        `primary: NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")"`
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
