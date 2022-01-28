import re
import warnings
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

        self.has_includes = False
        self.n_included_lines = 0
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
        seen_imports: set[Path] = set()  # Track fully resolved import paths
        out_src = self.in_src.splitlines(keepends=True)
        for idx, line in enumerate(out_src):
            if line.strip():  # Ignore empty lines
                if include := INCLUDE_DIRECTIVE.search(line):
                    match include.group(1)[0]:
                        case "<":
                            # Pylox builtin
                            module_name = include.group(1).strip("<>")
                            module_path = (BUILTINS_PATH / f"{module_name}.lox").resolve()
                        case "'" | '"':
                            # Path to source file
                            module_name = include.group(1).strip("'\"")
                            module_path = Path(module_name).resolve()
                        case _:
                            raise ValueError(f"Unknown include prefix: '{include.group(1)[0]}'")

                    incoming_src = load_if_exists(module_path)
                    out_src[idx] = incoming_src

                    # Subtract 1 line since we're replacing the line with the include directive
                    self.n_included_lines += incoming_src.count("\n") - 1

                    if module_path in seen_imports:
                        warnings.warn(
                            f"Duplicate include founds: '{include.group(1)}'",
                            ImportWarning,
                        )
                    seen_imports.add(module_path)

                else:
                    # End of include block reached
                    break

        # Check once rather than every time we matched an include directive
        if seen_imports:
            self.has_includes = True

        self.resolved_src = "".join(out_src)
