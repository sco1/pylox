import re
from pathlib import Path

INCLUDE_DIRECTIVE = re.compile(r"include\s+([\"\'\<].+[\"\'\>])$")

BUILTINS_PATH = Path(__file__).parent / "builtins"
if not BUILTINS_PATH.exists():
    raise OSError(f"Could not locate builtins directory, expected: '{BUILTINS_PATH.resolve()}'")


def load_if_exists(filepath: Path) -> str:
    """If a file exists, return its contents, otherwise raise an error."""
    if not filepath.exists():
        raise ValueError(f"Could not locate source file: '{filepath}'")

    return filepath.read_text()


class PreProcessor:
    """
    The Pylox preprocessor!

    Currently this only handles `include` statments.
    """

    resolved_src: str

    def __init__(self, src: str) -> None:
        self.in_src = src
        self.resolve_source()

    def resolve_source(self) -> None:
        """
        Resolve any `include` statements found in the header of the provided source.

        `include` statements are currently constrained as follows:
            * Statements may be specified in one of the following ways:
                * `include "path/to/src"`
                    * Attempts to copy from a source file at the given absolute or relative path
                * `include <lox_builtin>`
                    * Attempts to copy from a "stdlib" source file with name `<lox_builtin>.lox` in
                    the `./pylox/builtins/` directory
            * `include` statements are only found at the beginning of the source file, and may be
            separated by whitespace
            * One path per `include` line
            * Referenced source files do not themselves have any imports
        """
        out_src = self.in_src.splitlines(keepends=True)
        for idx, line in enumerate(out_src):
            if line.strip():  # Ignore empty lines
                if include := INCLUDE_DIRECTIVE.search(line):
                    match include.group(1)[0]:
                        case "<":
                            # Pylox builtin
                            module_name = include.group(1).strip("<>")
                            out_src[idx] = load_if_exists(BUILTINS_PATH / f"{module_name}.lox")
                        case "'" | '"':
                            # Path to source file
                            module_name = include.group(1).strip("'\"")
                            out_src[idx] = load_if_exists(Path(module_name))
                else:
                    # End of include block reached
                    break

        self.resolved_src = "".join(out_src)
