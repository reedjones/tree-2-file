"""Console script for tree_2_file."""
import os

import pyperclip
import tree_2_file

import typer
from rich.console import Console

from tree_2_file.tree_2_file import format_directory_tree, interactive, parse_structure

app = typer.Typer()
console = Console()


@app.command()
def main(
    file: str = typer.Option(None, "-f", "--file", help="Read from a file containing the directory structure"),
    raw: str = typer.Option(None, "-r", "--raw", help="Read the directory structure from text"),
    format_tree: bool = typer.Option(False, "-t", "--format-tree", help="Format the input as a markdown directory tree"),
    skip_root: bool = typer.Option(False, "-s", "--skip-root", help="Skip the root directory"),
    clip: bool = typer.Option(False, "-c", "--clip", help="Read the directory structure from the clipboard"),
    no_check: bool = typer.Option(False, "-n", "--no-check", help="Confirm before generating"),
    interactive_mode: bool = typer.Option(False, "-i", "--interactive", help="Run interactive mode"),
    step_through: bool = typer.Option(False, "-x", "--step-through", help="Run step-through mode"),
    dry: bool = typer.Option(False, "-d", "--dry", help="Dry run (doesn't create files)"),
):
    structure = None
    
    if interactive_mode:
        interactive()
    
    if file and os.path.isfile(file):
        with open(file, "r") as f:
            structure = f.read()
    elif raw:
        structure = raw
    elif clip:
        structure = pyperclip.paste()
    
    if not structure:
        console.print("! :warning: Didn't get any input. See help :skull:", style="danger")
        raise typer.Exit()
    
    sr = skip_root

    if format_tree:
        console.print("Will re-format input as proper markdown tree")
        old_format = structure
        new_format = format_directory_tree(structure)
        console.print(f"{old_format} \n{new_format}")
    
    if not no_check:
        console.print(f"Path is {os.getcwd()}")
        response = typer.prompt(
            f":open_file_folder: :warning: Will generate the following files/directories \n {structure} \n Will skip root: {sr} \n Press y|Y to continue, n|N or esc to exit",
            type=str,
        )
        if response.lower() != "y":
            console.print("Leaving")
            raise typer.Exit()
        console.print("Running")
    
    parse_structure(structure, skip_root=sr, dry=dry)

if __name__ == "__main__":
    app()
