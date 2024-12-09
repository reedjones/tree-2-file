"""Main module."""
import os
import sys
from rich.emoji import Emoji
from rich.tree import Tree

import argparse
from typing import List
import pyperclip
from rich import print

from rich.prompt import Confirm, Prompt
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.markup import escape
from rich.theme import Theme

custom_theme = Theme({"info": "dim cyan", "warning": "magenta", "danger": "bold red"})
console = Console(theme=custom_theme)


def display_columns(text1, text2, titles: List[str] = None):
    """
    Displays two blocks of text side by side in columns using rich.
    """
    if not titles:
        titles = ["column 1", "column 2"]
    titles = [i.capitalize() for i in titles]

    column1 = Panel(text1, title=titles[0], border_style="blue")
    column2 = Panel(text2, title=titles[1], border_style="green")

    columns = Columns([column1, column2])
    console.print(columns)


import re
from pathlib import Path


def clean_path(path):
    """
    Clean the given path by removing any characters that are not valid for file or directory names.

    Parameters:
    path (str): The input path to be cleaned.

    Returns:
    str: The cleaned path.
    """
    # Define a regex pattern to match unwanted characters (e.g., └──, │, ├──, etc.)
    pattern = re.compile(r"[│└──├── ]+")

    # Substitute unwanted characters with an empty string
    cleaned_path = re.sub(pattern, "", path)

    pattern2 = re.compile(r"[│└├─── ]+")
    cleaned_path = re.sub(pattern2, "", cleaned_path)

    return cleaned_path


def clean_path2(path):
    return (
        path.replace("├──", "")
        .replace("├", "")
        .replace("|", "")
        .replace("└──", "")
        .strip()
    )


def get_icon(path: str, tree: Tree = None):
    if "." in path:
        icon = "🐍 " if path.suffix == ".py" else "📄 "
    else:
        icon = "📁"
    return icon


def add_to_tree(path: str, tree: Tree = None):
    icon = get_icon(path)
    tree.add(Text(icon) + path)
    console.print(tree)


def print_path(path):
    icon = get_icon(path)
    console.print(Text(icon) + path)


def add_to_tree2(path, is_dir, tree: Tree):
    path = Path(path)
    if is_dir:
        style = "dim" if path.name.startswith("__") else ""
        tree.add(
            Text.from_markup(
                f"[bold magenta] :open_file_folder: [link file://{path}]{escape(path.name)}",
            ),
            style=style,
            guide_style=style,
        )
    else:
        text_filename = Text(path.name, "green")
        text_filename.highlight_regex(r"\..*$", "bold red")
        text_filename.stylize(f"link file://{path}")
        icon = "🐍 " if path.suffix == ".py" else "📄 "
        tree.add(Text(icon) + text_filename)
    console.print(tree)


class Node:
    def __init__(self, name, is_dir=False, is_root=False):
        print(f"createing node with name {name}")
        self.name = clean_path(name)
        print(self.name)
        self.is_dir = is_dir
        self.children = []
        self.is_root = is_root
        if is_root:
            self.tree = Tree(
                Text.from_markup(
                    f":open_file_folder: [link file://{name}",
                ),
                guide_style="bold bright_blue",
            )
            print(self.tree)

    def add_child(self, node):
        self.children.append(node)
        if self.is_root:
            add_to_tree(node.name, node.is_dir, self.tree)


def detect_mixed_indentation(line: str) -> bool:
    return " " in line and "\t" in line


def calculate_indent_level_with_tree(line: str, spaces_per_indent: int = 4) -> int:
    # Strip leading non-space characters like '│', '├──', '└──' to count spaces
    line_without_tree_chars = line.lstrip("│ ──")

    # Count the leading spaces after stripping out the tree characters
    leading_spaces = len(line) - len(line_without_tree_chars)

    # Calculate the indent level based on spaces
    indent_level = leading_spaces // spaces_per_indent
    return indent_level


import re


def calculate_indent_level(line: str, spaces_per_indent: int = 4) -> int:
    # Strip leading tree characters such as '│', '├──', '└──' using regex
    line_without_tree_chars = re.sub(r"^[│├└──\s]*", "", line)

    # Count the leading spaces
    leading_spaces = len(line) - len(line_without_tree_chars)

    # Calculate the indent level based on spaces
    indent_level = leading_spaces // spaces_per_indent
    return indent_level


def parse_structure(
    structure, skip_root=False, dry=False, log_actions=False, do_debug=False
):
    def is_safe_path(base_path: Path, given_path: Path) -> bool:
        resolved_path = (base_path / given_path).resolve()
        return base_path.resolve() in resolved_path.parents

    # structure = structure.strip().replace("\r", "\n")
    lines = structure.strip().splitlines()
    print("lines \n base")
    print(lines)
    base_path = Path.cwd()
    print(base_path)

    if skip_root:
        root_dir = lines.pop(0).strip("/").strip()
        print("lines \n root ")
        print(lines)
        print(root_dir)
    else:
        root_dir = lines[0].strip("/").strip()
        root_dir = clean_path(root_dir)
        lines = lines[1:]
        print("lines \n root \n base ")
        print(lines)
        print(root_dir)
        base_path = base_path / root_dir
        print(base_path)
        if not dry:
            base_path.mkdir(parents=True, exist_ok=True)
        if dry or log_actions:
            console.print(f"mkdir: {base_path}")

    path_stack = [base_path]
    print("path stack: ")
    print(path_stack)

    for line in lines:
        print("indent level: ")
        print(calculate_indent_level(line))
        # print("with tree: ")
        # print(calculate_indent_level_with_tree(line))
        # Calculate the current indentation level
        normalized_line = line.expandtabs(4)
        # print(f"line: {line} \n normal: {normalized_line}")
        indent_level = calculate_indent_level(line)
        # print(f"line: {line} , indent : {indent_level}")
        line = re.sub(r"^[\|\s]*[├─└]*\s*", "", line).strip()
        if "#" in line:
            line = line.split("#")[0]
        is_dir = line.endswith("/")
        name = line.strip("/")
        # print(f"line: {line} , indent : {indent_level}, name: {name}, isdir: {is_dir}")
        if not name:
            print("no name found")
            continue

        name = clean_path(name)
        # print(f"name {name}")
        # Adjust the path stack to match the current indentation level
        while len(path_stack) > indent_level + 1:
            print(f"path_stack {path_stack}")
            path_stack.pop()

        # Determine the current path
        current_path = path_stack[-1] / name
        print(f"current path: {current_path}")
        if not is_safe_path(Path.cwd(), current_path):
            console.print(
                Text.from_markup(
                    f"[! :warning:] Directory traversal detected: {current_path}"
                ),
                style="danger",
            )
            continue

        if is_dir:
            if not dry:
                current_path.mkdir(parents=True, exist_ok=True)
            if dry or log_actions:
                console.print(f"mkdir: {current_path}")
            path_stack.append(current_path)
        else:
            if not dry:
                current_path.touch()
            if dry or log_actions:
                console.print(f"touch: {current_path}")


# Example usage:
tree_str = """
test_dir/
    ├── components/
    │   ├── Tool/
    │   │   ├── Tool.js
"""

# parse_structure(tree_str, dry=True, log_actions=True)


def format_directory_tree(tree_str):

    lines = tree_str.strip().split("\n")
    indent_level = 0
    markdown_tree = []
    stack = []

    for line in lines:
        stripped_line = line.lstrip()
        current_level = (len(line) - len(stripped_line)) // 4

        if current_level > indent_level:
            stack.append("    " * indent_level)
        elif current_level < indent_level:
            stack = stack[:current_level]

        markdown_line = "".join(stack) + "├── " + stripped_line
        markdown_tree.append(markdown_line)
        indent_level = current_level

    return "\n".join(markdown_tree).replace("├── ", "└── ", 1)


def test_create_tree():
    console.rule("[bold yellow]Test Create Tree")
    # Example usage:
    tree_str = """\
my_map_app/
    app.py
    templates/
        map.html
    static/
        css/
            styles.css
        js/
            map.js
    """
    # print(tree_str)
    formatted_tree = format_directory_tree(tree_str)
    # print(formatted_tree)
    display_columns(tree_str, formatted_tree, titles=["Original", "Transformed"])
    parse_structure(
        formatted_tree, skip_root=False, dry=True, log_actions=True, do_debug=True
    )


test_structure = """
        test_dir/
        ├── components/
        │   ├── Tool/
        │   │   ├── Tool.js
        │   │   ├── Form.js
        │   ├── Component/
        │   │   ├── Component.js
        │   │   ├── Form.js
        │   │   ├── DeleteDialog.js
        │   │   ├── Export.js
        │   ├── Dashboard/
        │   │   ├── Dashboard.js
        │   │   ├── List.js
        │   │   ├── Panel.js
        ├── state/
        │   ├── Store.js
        ├── App.js
        ├── index.js
        """


def test_run():
    parse_structure(test_structure)
    test_create_tree()
    console.rule("[bold yellow]Test Parse Structure")

    parse_structure(test_structure, skip_root=False, dry=True, do_debug=True)
    exit()


from rich.table import Table


def interactive():
    console = Console()
    console.print(Emoji("test_tube"), "Welcome to the Directory Generator!")
    console.print(
        "This program will parse a directory structure and create files and directories."
    )

    # Create a table for the menu options
    table = Table(title="Menu")
    table.add_column("Option")
    table.add_column("Description")
    table.add_row("1", "Read structure from a file")
    table.add_row("2", "Read structure from text")
    table.add_row("3", "Read structure from clipboard")
    table.add_row("4", "Format input as a markdown directory tree")
    table.add_row("5", "Exit")

    # Display the menu table
    console.print(Panel(table, title="Menu Options"))

    # Prompt the user to choose an option
    option = Prompt.ask(
        "Please choose an option (1/2/3/4/5): ",
        console=console,
    )

    if option == "1":
        # Read structure from a file
        file_path = Prompt.ask(
            "Enter the path to the file: ",
            console=console,
        )
        # Implement file reading and processing logic here
        console.print(f"Reading structure from file: {file_path}")

        # ...
    elif option == "2":
        # Read structure from text
        structure = Prompt.ask(
            "Enter the directory structure: ",
            console=console,
        )
        # Implement text parsing and processing logic here
        console.print(f"Reading structure from text:\n{structure}")
        # ...
    elif option == "3":
        # Read structure from clipboard
        import pyperclip

        structure = pyperclip.paste()
        console.print("Reading structure from clipboard:")
        console.print(structure)
        # Implement clipboard parsing and processing logic here
        # ...
    elif option == "4":
        # Format input as a markdown directory tree
        structure = Prompt.ask(
            "Enter the directory structure: ",
            console=console,
        )
        # Implement markdown tree formatting logic here
        formatted_structure = format_directory_tree(structure)
        console.print(f"Formatted structure:\n{formatted_structure}")
        # ...
    elif option == "5":
        # Exit the program
        console.print("Exiting the Directory Generator.")
        exit()
    else:
        console.print("Invalid option selected. Please try again.")
        interactive()


def main():
    console.log()
    parser = argparse.ArgumentParser(
        description="Parse directory structure and create files and directories."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Read from a file containing the directory structure",
        default=None,
    )
    parser.add_argument(
        "-r",
        "--raw",
        type=str,
        default=None,
        help="Read the directory structure from text",
    )
    parser.add_argument(
        "-t",
        "--format-tree",
        default=False,
        action="store_true",
        help="Format the input as a markdown directory tree (adds missing `├──` chars)",
    )
    parser.add_argument(
        "-s",
        "--skip-root",
        action="store_true",
        help="Skip the root directory",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--clip",
        default=False,
        action="store_true",
        help="Read the directory structure from the clipboard",
    )
    parser.add_argument(
        "-n",
        "--no-check",
        action="store_true",
        default=False,
        help="confirm before generating",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="run interactive mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-x",
        "--step-through",
        help="run step through mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-d",
        "--dry",
        default=False,
        action="store_true",
        help="dry run (doesn't create files)",
    )
    structure = None
    args = parser.parse_args()
    if args.interactive:
        interactive()
    if args.file and os.path.isfile(args.file):
        with open(args.file, "r") as f:
            structure = f.read()
    elif args.raw:
        structure = args.raw
    elif args.clip:
        structure = pyperclip.paste()
    if not structure:

        console.print(
            "! :warning: Didn't get any input see help :skull:", style="danger"
        )
        exit()
    sr = False

    if args.skip_root:
        sr = True
    if args.format_tree:
        console.print("Will re-format input as proper markdown tree")
        old_format = structure
        new_format = format_directory_tree(structure)
        console.print(f"{old_format} {new_format}")
    if not args.no_check:
        console.print(f"path is {os.getcwd()}")
        response = input(
            f":open_file_folder: :warning: Will generate the following files/directories \n {structure} \n Will skip root: {sr} \n Press y|Y to continue, n|N or esc to exit"
        )
        if not response in ["y", "Y"]:
            console.print("leaving")
            exit()
        console.print("running")

    parse_structure(structure, skip_root=sr, dry=args.dry)


if __name__ == "__main__":
    main()
