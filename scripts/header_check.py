#!/usr/bin/env python

"""
File docstring header check
===========================

**August 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com) : Initial design

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.

This script checks that the python file header matches a specific,
consistent header format, with various rules.
"""

from __future__ import annotations

from pathlib    import Path

from argparse import ArgumentParser
from datetime import date

from parsimonious.grammar import Grammar
from parsimonious.nodes   import NodeVisitor
from dataclasses          import dataclass

from pprint import pprint

import ast
import textwrap
import sys


# ---------------------------------------------- Exceptions

class RuleError(Exception):
    def __init__(self, rule_name: str, explanation: str):
        super().__init__(f"Rule [{rule_name}] did not match: {explanation}")


# ---------------------------------------------- Grammar for docstring structure parsing

_GRAMMAR = Grammar(
    r"""
    docstring_format    = main_title main_date main_authors license description

    main_title          = md_h1_title emptyline+
    md_h1_title         = title_text nl title_underline

    title_text          = text+
    title_underline     = equal+

    main_date           = "**" month ws+ year "**" emptyline+
    
    main_authors        = author+ emptyline+
    author              = "-" ws+ author_name ws+ author_mail author_contrib_opt emptyline
    author_name         = (ws* word)+
    author_mail         = "(" email ")"
    author_contrib_opt  = author_contribution?
    author_contribution = ws* ":" ws* text+

    license             = license_line+
    license_line        = ">" ws* text+ nl

    description         = emptyline* (~r"[^>]" text+ emptyline*)*

    month               = word+
    year                = number{4}

    email               = local "@" domain
    local               = ~r"[a-zA-Z0-9._%+-]+"
    domain              = subdomain ("." subdomain)*
    subdomain           = ~r"[a-zA-Z0-9-]+"

    emptyline           = ws* nl
    number              = ~r"[0-9]"
    equal               = ~r"="
    text                = ~r"[^\n\r]"
    word                = ~r"\w"
    ws                  = ~r"[ \t]"
    nl                  = ~r"[\n\r]"
    """
)


# ---------------------------------------------- Dataclasses for file header structure

@dataclass
class FileHeaderAuthor:
    name: str
    mail: str
    contribution: str | None = None


@dataclass
class FileHeaderDate:
    month: str
    year: int

@dataclass
class FileHeaderTitle:
    text: str
    underline: str

@dataclass
class FileHeaderInfo:
    main_title: FileHeaderTitle
    main_authors: list[FileHeaderAuthor]
    main_date: FileHeaderDate
    license: str
    description: str


# ---------------------------------------------- Node visitor for structure parsing

class FileHeaderVisitor(NodeVisitor):
    def __init__(self):
        super().__init__()

    def visit_docstring_format(self, node, visited_children):
        return FileHeaderInfo(
            main_title   = visited_children[0],
            main_authors = visited_children[2],
            main_date    = visited_children[1],
            license      = visited_children[3],
            description  = visited_children[4],
        )

    def visit_main_title(self, node, visited_children):
        return FileHeaderTitle(
            text      = visited_children[0][0],
            underline = visited_children[0][1],
        )

    def visit_md_h1_title(self, node, visited_children):
        return (visited_children[0], visited_children[2])

    def visit_title_text(self, node, visited_children):
        return node.text

    def visit_title_underline(self, node, visited_children):
        return node.text

    def visit_main_fields(self, node, visited_children):
        return visited_children[0]

    def visit_main_field(self, node, visited_children):
        return node.children[2].text

    ###

    def visit_main_authors(self, node, visited_children):
        return visited_children[0]

    def visit_author(self, node, visited_children):
        return FileHeaderAuthor(
            name         = visited_children[2],
            mail         = visited_children[4],
            contribution = visited_children[5]
        )

    def visit_author_name(self, node, visited_children):
        return node.text

    def visit_author_mail(self, node, visited_children):
        return visited_children[1]

    def visit_author_contrib_opt(self, node, visited_children):
        return visited_children[0] if visited_children else None

    def visit_author_contribution(self, node, visited_children):
        return node.children[3].text.strip()

    def visit_main_date(self, node, visited_children):
        return FileHeaderDate(
            month = visited_children[1],
            year  = int(visited_children[3])
        )

    def visit_description(self, node, visited_children):
        return node.text

    def visit_license(self, node, visited_children):
        return " ".join(visited_children)

    def visit_license_line(self, node, visited_children):
        return node.children[2].text

    def visit_month(self, node, visited_children):
        return node.text

    def visit_year(self, node, visited_children):
        return node.text

    def visit_email(self, node, visited_children):
        return node.text

    def generic_visit(self, node, visited_children):
        return visited_children or node


# ---------------------------------------------- Utilities

def extract_docstring(file_path):
    """
    Extracts the docstring from a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        str: The docstring of the file, or None if no docstring is found.
    """

    try:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())
            docstring = ast.get_docstring(tree)
            return docstring

    except Exception as exc:
        raise RuleError("extract_docstring", f"Failed to extract docstring: {exc!s}")


def parse_header(docstring: str):
    try:
        parsed_structure = _GRAMMAR.parse(docstring + "\n") # trailing \n is added to avoid parser errors.
        visitor = FileHeaderVisitor()
        result = visitor.visit(parsed_structure)

        return result

    except Exception as exc:
        raise RuleError("parse_header", f"Failed to parse file structure: {exc!s}")

# ---------------------------------------------- Rules

def rule_check_underline_length(fh: FileHeaderInfo):
    len_text  = len(fh.main_title.text)
    len_under = len(fh.main_title.underline)

    if len_text != len_under:
        raise RuleError("rule_check_underline_length", f"length of title underline ({len_under}) doesn't match the length of title text ({len_text})")

def rule_check_month(fh: FileHeaderInfo):
    _MONTHS = {
        "January",
        "February",
        "March",
        "April",
        "May",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    }

    if not fh.main_date.month in _MONTHS:
        raise RuleError("rule_check_month", f"{fh.main_date.month} is not a valid month (Accepted: {', '.join(_MONTHS)}")

def rule_check_year(fh: FileHeaderInfo):
    today        = date.today()
    current_year = today.year

    year_start   = 2024

    if not fh.main_date.year in range(year_start, current_year+1):
        raise RuleError("rule_check_year", f"{fh.main_date.year} is not in correct year range: {year_start}-{current_year}")

def rule_check_license(fh: FileHeaderInfo):
    TEXT = "This file is part of the Overity.ai project, and is licensed under the terms of the Apache 2.0 license. See the LICENSE file for more information."

    if fh.license != TEXT:
        raise RuleError("rule_check_license", "License text doesn't correspond to expected value.")


# ---------------------------------------------- Check a a single file

def file_check(path):
    print(f"> Check file: {path}... ", end="")

    try:
        docstring = extract_docstring(path)
        header_struct = parse_header(docstring)

        rule_check_month(header_struct)
        rule_check_year(header_struct)
        rule_check_underline_length(header_struct)
        rule_check_license(header_struct)

        print("OK")
        return True

    except RuleError as exc:
        print("Fail")
        print(f"--> {exc!s}")
        print("")
        return False

# ---------------------------------------------- Main program

if __name__ == "__main__":
    parser = ArgumentParser(description="Check file header")
    parser.add_argument("path", help="Path to input file or folder to check")
    args = parser.parse_args()

    path = Path(args.path)

    output_status = True

    if path.is_file():
        output_status = file_check(path)

    elif path.is_dir():
        print(f"Check folder: {path}")

        for fpath in path.rglob("*.py"):
            # If the file check is failed, output_status will be false,
            # and will stay false afterwards.
            output_status = output_status and file_check(fpath)
    else:
        RuntimeError(f"{path} is neither a file or a folder, does it exist?")

    # Setting exit code
    sys.exit(
        0 if output_status else -1
    )
