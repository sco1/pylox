from pathlib import Path
from textwrap import dedent

import typer
from rich import print

testgen_cli = typer.Typer()
CURRENT_DIR = Path()


FILE_TEMPLATE = dedent(
    """\
    from textwrap import dedent

    import pytest

    from pylox.lox import Lox

    # Base cases from https://github.com/munificent/craftinginterpreters/blob/master/test/{module}/{name}.lox
    TEST_SRC = dedent(
        \"\"\"\\
    {src}
        \"\"\"
    )

    EXPECTED_STDOUTS = [...]


    @pytest.mark.xfail(reason="Autogenerated test skeleton")
    def test_{name}(capsys: pytest.CaptureFixture) -> None:
        interpreter = Lox()
        interpreter.run(TEST_SRC)

        assert not interpreter.had_error
        assert not interpreter.had_runtime_error

        all_out = capsys.readouterr().out.splitlines()
        assert all_out == EXPECTED_STDOUTS
    """
)


@testgen_cli.command()
def main(
    module_name: str,
    input_dir: Path = typer.Argument(default=CURRENT_DIR),
    output_dir: Path = typer.Argument(default=CURRENT_DIR),
) -> None:
    """
    Automatically generate test skeletons from the provided directory of lox tests.

    For each `*.lox` file in the provided directory:
        * A `test_<filename>.py` file is created
        * The lox source code from `filename.lox` is added to a `textwrap.dedent` call
        * An empty `def test_<filename>()` function is created
    """
    for filepath in input_dir.glob("*.lox"):
        name = filepath.stem

        # Indent the source once to line up with the dedent quotes
        lox_src = "\n".join(
            f"    {line}".rstrip() for line in filepath.read_text().rstrip().splitlines()
        )

        out_filepath = output_dir / module_name / f"test_{name}.py"
        out_filepath.parent.mkdir(exist_ok=True)
        print(f"Generating '{out_filepath}' ...")
        out_filepath.write_text(FILE_TEMPLATE.format(name=name, module=module_name, src=lox_src))


if __name__ == "__main__":
    testgen_cli()
