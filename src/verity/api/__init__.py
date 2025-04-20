"""
VERITY API for method writing
=============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

import logging
import inspect
from pathlib import Path

from verity.backend import flow

# Initialize global flow object
_CTX = flow.FlowCtx.default()


def init():
    # Initialize logging facilities
    # TODO: Improve logging format, and add environment variable for debug
    logging.basicConfig(level=logging.INFO)

    # Get caller method file name
    caller_frame = inspect.stack()[1]
    caller_fpath = Path(caller_frame.filename)

    # Call flow init.
    flow.init(_CTX, caller_fpath)
