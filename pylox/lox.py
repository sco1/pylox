import typing as t
from pathlib import Path

import typer
from rich import print
from rich.prompt import Prompt

from pylox.error import LoxException
from pylox.scanner import Scanner

pylox_cli = typer.Typer()
Prompt.prompt_suffix = ""  # Get rid of the default colon suffix


class Lox:
    def __init__(self) -> None:
        self.had_error = False

    def run_file(self, src_filepath: Path) -> None:
        src = src_filepath.read_text()
        self.run(src)

    def run_prompt(self) -> None:
        while True:
            line = Prompt.ask(">>> ")
            self.run(line)

    def run(self, src: str) -> None:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()

        print(tokens)

    def report(self, err: LoxException) -> None:
        print(f"{err.line}:{err.col}: [bold red]{err}[/bold red]")
        self.had_error = True


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
