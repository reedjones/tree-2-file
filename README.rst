======================
Text Tree 2 Filesystem
======================


.. image:: https://img.shields.io/pypi/v/tree_2_file.svg
        :target: https://pypi.python.org/pypi/tree_2_file

.. image:: https://img.shields.io/travis/reedjones/tree_2_file.svg
        :target: https://travis-ci.com/reedjones/tree_2_file

.. image:: https://readthedocs.org/projects/tree-2-file/badge/?version=latest
        :target: https://tree-2-file.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


This project provides a tool for generating directories and files from a given structure. It supports interactive and command-line interfaces, allowing you to create directories from text, file input, clipboard, or even format input into a markdown-style directory tree.

## Features

- **CLI Support**: Use various command-line arguments to generate directories from file input, text, or clipboard.
- **Interactive Mode**: Navigate through a simple menu to select options like reading structure from a file or formatting it into a markdown tree.
- **Rich Console**: Beautiful, colorful output for better readability.

## Installation

1. Install with pip:

`bash
pip install tree-2-file
`

2. Clone the repository:

`bash
git clone https://github.com/yourusername/directory-generator.git
cd directory-generator
pip install -r requirements.txt
`



* Free software: MIT license
* Documentation: https://tree-2-file.readthedocs.io.


Features
--------

Features
========

- **Directory Structure Parsing**:
  - Parse and process directory structures from various sources including:
    - Files
    - Text input
    - Clipboard
  - Handle complex directory hierarchies with different indentations.

- **File and Directory Creation**:
  - Create directories and files based on the parsed structure.
  - Option to simulate file and directory creation (dry-run) without making any changes.

- **Markdown Directory Tree Formatting**:
  - Automatically format directory structures into markdown-style trees, adding missing `├──` characters for proper tree representation.

- **Rich Console Output**:
  - Utilize the `rich` library to display output with enhanced formatting, including:
    - Columns for side-by-side content display.
    - Colored and stylized text for better readability.
    - Themed console output for various log levels (info, warning, danger).

- **Interactive CLI**:
  - Fully interactive CLI interface allowing the user to choose how to read directory structure:
    - From a file.
    - From direct text input.
    - From clipboard content.
    - Format the structure as markdown.
  - User-friendly menu and prompt-based navigation.

- **Clipboard Support**:
  - Ability to parse directory structures directly from the clipboard, making it easy to work with copied content.

- **Tree Visualization**:
  - Dynamically generate and display tree-like structures in the console, including icons for files and directories:
    - Python files (`.py`) represented with a snake icon.
    - Other files with a document icon.
    - Directories with a folder icon.

- **Custom Themes and Console Styling**:
  - Define custom themes using the `rich` library to customize console appearance.
  - Provide a variety of styles for different types of messages (e.g., success, warning, error).

- **Log Actions and Debugging**:
  - Log actions taken during the parsing and file creation process for debugging or dry-run scenarios.
  - Option to log the creation of files and directories (e.g., `mkdir`, `touch`).

Credits
-------

creator - Reed Jones https://github.com/reedjones 

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
