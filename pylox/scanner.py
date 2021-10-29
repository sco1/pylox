from pylox.error import LoxSyntaxError
from pylox.protocols import InterpreterProtocol
from pylox.tokens import LITERAL_T, Token, TokenType

RESERVED = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def is_alpha(char: str) -> bool:
    """Create a custom "is alphabetic" checker, as `str.isalpha` doesn't include underscores."""
    return any(
        (
            "a" <= char <= "z",
            "A" <= char <= "Z",
            char == "_",
        )
    )


def is_alnum(char: str) -> bool:
    """Create a custom "is alphanumeric" checker, as `str.alnum` doesn't include underscores."""
    return any(
        (
            is_alpha(char),
            char.isdigit(),
        )
    )


class Scanner:
    """The pylox tokenizer."""

    def __init__(self, src: str, interpreter: InterpreterProtocol) -> None:
        self.src = src
        self._interpreter = interpreter
        self.tokens: list[Token] = []

        # Keep track of where the scanner is in the source
        # Source is not split by newlines, so indices are relative to the full source string
        self._start = 0  # Index of first character in lexeme
        self._current = 0  # Index of current character being considered
        self._lineno = 0
        self._line_start = 0  # Index of the start of the current line in the full source string

    @property
    def _col_offset(self) -> int:
        """Return the column offset relative to the beginning of the current line."""
        return self._start - self._line_start

    def _bump_line(self) -> None:
        """Bump the current line index & update the offset for the start of the current line."""
        self._lineno += 1
        self._line_start = self._current

    def _is_eof(self) -> bool:
        """Check if the scanner has reached the end of the source."""
        return self._current >= len(self.src)

    def _advance(self) -> str:
        """Return the next character to be consumed by the scanner & advance the scan pointer."""
        self._current += 1
        return self.src[self._current - 1]

    def _peek(self, offset: int = 0) -> str:
        """
        Return the next character to be consumed, without advancing the scan pointer ("lookahead").

        An integer `offset` may be specified to look further ahead in the source; this offset is
        0-indexed, where the default value of `0` will return the next character.
        """
        if self._is_eof():
            return "\0"

        return self.src[self._current + offset]

    def _match_next(self, check_char: str) -> bool:
        """Consume the next source character & check if it matches the specified check character."""
        if self._is_eof():
            return False

        # When we consume a character we advance `current`, so we don't need to adjust the index
        if self.src[self._current] == check_char:
            self._advance()
            return True
        else:
            return False

    def _string(self, close: str) -> None:
        """
        Handle string literal token generation.

        The `close` kwarg specifies the type of closing quotation to expect (`"` or `'`).
        """
        # Consume characters until we get to the corresponding closing quote
        # If we get to the end of the file before the quote is closed, raise an error
        while not any((self._peek() == close, self._is_eof())):
            if self._peek() == "\n":
                self._bump_line()

            self._advance()

        if self._is_eof():
            # String quotes were never closed, this should be a lox error
            raise NotImplementedError

        self._advance()  # Consume the closing quote
        literal = self.src[self._start + 1 : self._current - 1]  # Index away the quotation marks

        self._add_token(TokenType.STRING, literal)

    def _number(self) -> None:
        """
        Handle numeric literal token generation.

        Both integers and floats are consumed into the single `NUMBER` token type & represented
        internally as Python `float` objects.

        NOTE: Leading & trailing decimals are not supported (e.g. `.123` and `123.`)
        """
        # Consume digits until we get to a non-digit
        while self._peek().isdigit():
            self._advance()

        # Check for fractional component
        # Use peek offset to check the character after the period
        if self._peek() == "." and self._peek(offset=1).isdigit():
            self._advance()  # Consume the period

            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.src[self._start : self._current]))

    def _identifier(self) -> None:
        """Handle identifier & keyword token generation."""
        while is_alnum(self._peek()):
            self._advance()

        # If the lexeme does not match a reserved keyword, then it is considered an identifier
        lexeme = self.src[self._start : self._current]
        token_type = RESERVED.get(lexeme, TokenType.IDENTIFIER)
        self._add_token(token_type)

    def _add_token(self, token_type: TokenType, literal: LITERAL_T = None) -> None:
        """
        Add a token of the specified type to the internal list of tokens.

        A `literal` value may be optionally provided for tokens that use it (e.g. `STRING`,
        `NUMERIC`)
        """
        self.tokens.append(
            Token(
                token_type=token_type,
                lexeme=self.src[self._start : self._current],
                literal=literal,
                lineno=self._lineno,
                col_offset=self._col_offset,
            )
        )

    def _scan_token(self) -> None:
        """Consume the next source character(s) & dispatch the appropriate token generation."""
        char = self._advance()
        match char:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                if self._match_next("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case "=":
                if self._match_next("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case "<":
                if self._match_next("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case ">":
                if self._match_next("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case "/":
                if self._match_next("/"):
                    # // begins a comment line; comments are discarded
                    # Consume characters until we get to the end of either the line or the file
                    while not any((self._peek() == "\n", self._is_eof())):
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # Ignore whitespace
                pass
            case "\n":
                self._bump_line()
            case '"' | "'":
                # String literals; can be defined by either `''` or `""`; may be multiline
                if char == '"':
                    close = '"'
                else:
                    close = "'"

                self._string(close)
            case _:
                # Catch numeric literals
                if char.isdigit():
                    self._number()
                elif is_alpha(char):
                    self._identifier()
                else:
                    self._interpreter.report_error(
                        LoxSyntaxError(
                            self._lineno,
                            self._col_offset,
                            f"Unsupported character encountered: '{char}'"
                        )
                    )

    def scan_tokens(self) -> list[Token]:
        """
        Scan through the loaded source code & generate a list of tokens.

        The list of tokens is stored internal to the scanner & also returned for external use.

        An `EOF` token is automatically added to the end of the file when it is reached.
        """
        while not self._is_eof():
            self._start = self._current
            self._scan_token()

        self.tokens.append(
            Token(
                token_type=TokenType.EOF,
                lexeme="",
                literal=None,
                lineno=self._lineno,
                col_offset=0,
            )
        )

        return self.tokens
