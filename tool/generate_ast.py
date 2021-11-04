import typing as t
from pathlib import Path
from textwrap import dedent

import typer
from rich import print

astgen_cli = typer.Typer()
CURRENT_DIR = Path()

IMPORT_BLOCK = dedent(
    """\
    # THIS FILE HAS BEEN AUTOGENERATED
    from __future__ import annotations

    import typing as t
    from abc import ABC, abstractmethod

    import attr

    from pylox.protocols import VisitorProtocol
    from pylox.tokens import LITERAL_T, Token"""
)

# Top level keys are classes that will subclass Expr
# Values are a dictionary of attribute, attribute type (as str) k,v pairs
SUBCLASS_T = dict[str, dict[str, str]]
EXPR_STRUCT = {
    "Assign": {"name": "Token", "value": "Expr"},
    "Binary": {"expr_left": "Expr", "token_operator": "Token", "expr_right": "Expr"},
    "Grouping": {"expr_expression": "Expr"},
    "Literal": {"object_value": "LITERAL_T"},
    "Logical": {"expr_left": "Expr", "token_operator": "Token", "expr_right": "Expr"},
    "Variable": {"name": "Token"},
    "Unary": {"token_operator": "Token", "expr_right": "Expr"},
}

STMT_STRUCT = {
    "Block": {"statements": "list[Stmt]"},
    "Expression": {"expr_expression": "Expr"},
    "If": {"condition": "Expr", "then_branch": "Stmt", "else_branch": "t.Optional[Stmt]"},
    "Var": {"name": "Token", "initializer": "t.Optional[Expr]"},
    "Print": {"expr_expression": "Expr"},
}

INDENT = "    "


def _gen_classdef(
    class_name: str,
    inherits_from: t.Optional[str] = None,
    class_attributes: t.Optional[dict[str, str]] = None,
    slotted: bool = True,
) -> str:
    """
    Generate a class definition from the provided components.

    If `inherits_from` is not specified, then the class is assumed to be an ABC.

    So we can support the visitor pattern, classes are given an `accept` method that calls a
    class-specific visitor method.

    NOTE: Multiple inheritance is not supported.
    NOTE: Class attributes must have a type specified (as str); empty strings will result in invalid
    syntax in the generated code.
    """
    print(f"{INDENT}Generating {class_name} class ...")
    components = []

    if inherits_from:
        # fmt: off
        components.append(
            (
                f"@attr.s(slots={slotted})\n"
                f"class {class_name}({inherits_from}):"
            )
        )
        # fmt: on
    else:
        components.append(f"class {class_name}(ABC):  # pragma: no cover")

    if class_attributes:
        components.extend(
            [
                f"{INDENT}{attribute}: {attribute_type} = attr.ib()"
                for attribute, attribute_type in class_attributes.items()
            ]
        )
    else:
        components.append(f"{INDENT}pass")

    components.append("")
    if inherits_from:
        components.append(
            (
                f"{INDENT}def accept(self, visitor: VisitorProtocol) -> t.Any:\n"
                f"{INDENT*2}return visitor.visit_{class_name}(self)"
            )
        )
    else:
        # Have base classes raise
        components.append(
            (
                f"{INDENT}@abstractmethod\n"
                f"{INDENT}def accept(self, visitor: VisitorProtocol) -> t.Any:\n"
                f"{INDENT*2}return NotImplemented"
            )
        )

    return "\n".join(components)


def define_ast(output_dir: Path, grammar_defs: dict[str, SUBCLASS_T]) -> None:
    """
    Generate a grammar module of syntax tree classes & output to the specified directory.

    `types` is a dictionary with class name, class attribute(s) k,v pairs. Class attributes must be
    specified as a dictionary of attribute, attribute type (as str) k,v pairs.

    A base class with `base_name` will be generated in the file, followed by classes built from the
    `types` dictionary. Classes generated from the `types` dictionary will all subclass the base
    class.

    A helper Protocol for the expected visitor pattern will also be created.
    """
    out_filename = output_dir / "grammar.py"
    print("Generating 'grammar.py' ...")

    out_src = [IMPORT_BLOCK]
    for base_name, types in grammar_defs.items():
        out_src.append(_gen_classdef(base_name))
        for child, attributes in types.items():
            out_src.append(_gen_classdef(child, base_name, attributes))

    # Build in 2 steps so we can add a newline to the end
    src = "\n\n\n".join(out_src)
    out_filename.write_text(f"{src}\n")


@astgen_cli.command()
def main(output_dir: Path = typer.Argument(default=CURRENT_DIR)) -> None:
    """Automatically generate the syntax tree classes & output to the specified directory."""
    print(f"Autogenerating AST module(s) into '{output_dir}' ...")
    define_ast(
        output_dir,
        {
            "Expr": EXPR_STRUCT,
            "Stmt": STMT_STRUCT,
        },
    )


if __name__ == "__main__":
    astgen_cli()
