import sys
import typing as t
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt

from pylox.error import LoxException, LoxRuntimeError
from pylox.interpreter import Interpreter
from pylox.parser import Parser
from pylox.preprocessor import PreProcessor
from pylox.resolver import Resolver
from pylox.scanner import Scanner

pylox_cli = typer.Typer()
Prompt.prompt_suffix = ""  # Get rid of the default colon suffix


class Lox:
    """The pylox interpreter core."""

    preprocessor: PreProcessor | None

    def __init__(self) -> None:
        self.interpreter = Interpreter(self)
        self.preprocessor = None

        self.had_error = False
        self.had_runtime_error = False

    def run_file(self, src_filepath: Path) -> None:
        """Execute the specified source file in the pylox interpreter."""
        src = src_filepath.read_text()
        self.run(src)

        if self.had_error:
            sys.exit(65)

        if self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self) -> None:
        """Enter into a pylox REPL."""
        while True:
            line = Prompt.ask(">>> ")
            self.run(line)

            # Reset these so we can stay in the REPL unhindered
            self.had_error = False
            self.had_runtime_error = False

    def run(self, src: str) -> None:
        """Run the specified source."""
        self.preprocessor = PreProcessor(src)

        scanner = Scanner(self.preprocessor.resolved_src, self)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, self)
        statements = parser.parse()

        # Don't run the resolver if we've had a scanning or parsing error, or if we didn't get any
        # statements
        if self.had_error or not statements:
            return

        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)

        # Don't run the resolver if we've had a scanning, parsing, or resolving error
        if self.had_error:
            return

        self.interpreter.interpret(statements)

    def _build_error_string(self, err: LoxException | LoxRuntimeError) -> str:
        """Adjust error location for any imports & make a colorful error."""
        line, col = err.line, err.col

        # Adjust the lineno to account for any inserted source code from include directive(s)
        # It would be good to eventually be able to associate this with the problematic import
        if self.preprocessor and self.preprocessor.has_includes:
            line -= self.preprocessor.n_included_lines

        return f"{line+1}:{col+1}: [bold red]{err}[/bold red]"

    def report_error(self, err: LoxException) -> None:
        """Report a general exception to the terminal."""
        print(self._build_error_string(err))
        self.had_error = True

    def report_runtime_error(self, err: LoxRuntimeError) -> None:
        """Report a runtime error to the terminal."""
        print(self._build_error_string(err))
        self.had_error = True
        self.had_runtime_error = True


@pylox_cli.command()
def main(lox_script: t.Optional[Path] = typer.Argument(default=None)) -> None:
    """
    Welcome to the pylox Lox interpreter!

    If a path to a Lox file is not provided, a pylox REPL will be opened.
    """
    lox = Lox()
    if not lox_script:
        # REPL
        lox.run_prompt()
    else:
        lox.run_file(lox_script)


if __name__ == "__main__":
    pylox_cli()
