"""
# Show program informations

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- March 2025
"""

from argparse import ArgumentParser, Namespace


def setup_parser(parser: ArgumentParser):
    subcommand = parser.add_parser(
        "infos", help="Get informations on program in current folder"
    )

    pass


def run(args: Namespace):
    print(args)
