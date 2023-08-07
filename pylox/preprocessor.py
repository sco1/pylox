import re
import typing as t
import warnings
from pathlib import Path

INCLUDE_DIRECTIVE = re.compile(r"include\s+([\"\'\<].+[\"\'\>])$")

BUILTINS_PATH = Path(__file__).parent / "builtins"
if not BUILTINS_PATH.exists():  # pragma: no cover
    raise OSError(f"Could not locate builtins directory, expected: '{BUILTINS_PATH.resolve()}'")


class IncludedHeader(t.NamedTuple):  # noqa: D101
    filepath: Path
    include_line: int  # Zero-indexed
    start_lineno: int  # Zero-indexed
    end_lineno: int  # Zero-indexed
    line_range: range  # range(start_lineno, end_lineno + 1)


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
    import_metadata: dict[IncludedHeader, None]

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
        # Track where included source comes from so we can track resolve error locations
        # Don't care about the values, just the keys
        self.import_metadata: dict[IncludedHeader, None] = {}
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
                        case _:  # pragma: no cover
                            raise ValueError(f"Unknown include prefix: '{include.group(1)[0]}'")

                    incoming_src = load_if_exists(module_path)
                    out_src[idx] = incoming_src

                    start_lineno = idx + self.n_included_lines
                    # Subtract 1 line since we're replacing the line with the include directive
                    self.n_included_lines += incoming_src.count("\n") - 1
                    end_lineno = idx + self.n_included_lines

                    metadata = IncludedHeader(
                        filepath=module_path,
                        include_line=idx,
                        start_lineno=start_lineno,
                        end_lineno=end_lineno,
                        line_range=range(start_lineno, end_lineno + 1),  # +1 to include end_lineno
                    )
                    self.import_metadata[metadata] = None

                    if module_path in seen_imports:
                        warnings.warn(
                            UserWarning(
                                f"Duplicate include founds: '{include.group(1)}'",
                                ImportWarning,
                            ),
                            stacklevel=2,
                        )
                    seen_imports.add(module_path)

                else:
                    # End of include block reached
                    break

        # Check once rather than every time we matched an include directive
        if seen_imports:
            self.has_includes = True

        self.resolved_src = "".join(out_src)
