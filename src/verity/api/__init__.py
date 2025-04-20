"""
VERITY API for method writing
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging
from pathlib import Path
from contextlib import contextmanager

from verity.backend import flow
from verity.errors import UnknownMethodError


# Initialize global flow object
_CTX = flow.FlowCtx.default()


def _get_method_path():
    # Strategy 1: if method is  python file
    try:
        import __main__

        return Path(__main__.__file__).resolve()
    except AttributeError:  # No __file__ -> Not from python file!
        pass

    # Strategy 2: called from VScode
    try:
        import __main__

        return Path(__main__.__vsc_ipynb_file__).resolve()
    except AttributeError:  # No __vsc_ipynb_file__ -> Not from VSCode!
        pass

    # No strategy worked, can't identify method
    raise UnknownMethodError()


def init():
    # Initialize logging facilities
    # TODO: Improve logging format, and add environment variable for debug
    logging.basicConfig(level=logging.INFO)

    caller_fpath = (
        _get_method_path()
    )  # Call the tricky thing to get the current method file path
    print(f"CALLER_FPATH={caller_fpath}")

    # Call flow init.
    flow.init(_CTX, caller_fpath)


@contextmanager
def describe_arguments():
    with flow.describe_arguments(_CTX) as vargs:
        yield vargs


def argument(name: str):
    return flow.argument(_CTX, name)
