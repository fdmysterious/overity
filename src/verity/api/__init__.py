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

from verity.backend.flow.ctx import FlowCtx, RunMode


# Initialize global flow object
_CTX = FlowCtx.default()


def _get_method_path():
    # Strategy 1: if method is python file
    try:
        import __main__

        return Path(__main__.__file__).resolve(), RunMode.Standalone
    except AttributeError:  # No __file__ -> Not from python file!
        pass

    # Strategy 2: called from VScode
    try:
        import __main__

        return Path(__main__.__vsc_ipynb_file__).resolve(), RunMode.Interactive
    except AttributeError:  # No __vsc_ipynb_file__ -> Not from VSCode!
        pass

    # No strategy worked, can't identify method
    raise UnknownMethodError()


def init():
    # Initialize logging facilities
    # TODO: Improve logging format, and add environment variable for debug
    logging.basicConfig(level=logging.INFO)

    caller_fpath, run_mode = _get_method_path()

    # Call flow init.
    flow.init(_CTX, caller_fpath, run_mode)


@contextmanager
def describe_arguments():
    with flow.describe_arguments(_CTX) as vargs:
        yield vargs


def argument(name: str):
    return flow.argument(_CTX, name)


def model_use(slug: str):
    return flow.model_use(_CTX, slug)


@contextmanager
def model_package(slug: str, exchange_format: str, target: str = "agnostic"):
    with flow.model_package(_CTX, slug, exchange_format, target) as vpkg:
        yield vpkg


def agent_use(slug: str):
    return flow.agent_use(_CTX, slug)


def metrics_save():
    return flow.metrics_save(_CTX)
