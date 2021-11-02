import sys
import typing as t
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt

from pylox.ast_printer import AstPrinter
from pylox.error import LoxException, LoxRuntimeError
from pylox.interpreter import Interpreter
from pylox.parser import Parser
from pylox.scanner import Scanner

pylox_cli = typer.Typer()
Prompt.prompt_suffix = ""  # Get rid of the default colon suffix


class Lox:
    """The pylox interpreter core."""

    def __init__(self) -> None:
        self.interpreter = Interpreter(self)

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
        """
        Run the specified source.

        Source is scanned into tokens, and that's it because we're only in Chapter 5. The tokens are
        printed for debugging purposes.
        """
        scanner = Scanner(src, self)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens, self)
        expr = parser.parse()

        prettyprinter = AstPrinter()
        print(prettyprinter.dump(expr))

        for_print, _ = self.interpreter.interpret(expr)
        print(for_print)

    def report_error(self, err: LoxException) -> None:
        """Report a general exception to the terminal."""
        print(f"{err.line+1}:{err.col+1}: [bold red]{err}[/bold red]")
        self.had_error = True

    def report_runtime_error(self, err: LoxRuntimeError) -> None:
        """Report a runtime error to the terminal."""
        print(f"{err.line+1}:{err.col+1}: [bold red]{err}[/bold red]")
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
