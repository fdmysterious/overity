"""
Manage arguments for methods
============================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from __future__ import annotations

import os

from verity.model.arguments import (
    Argument,
    Option,
    Flag,
    ArgumentSchema,
    OptionSchema,
    FlagSchema,
)
from verity.backend.flow.ctx import FlowCtx

from verity.errors import ArgumentNotFoundError, DuplicateArgumentNameError


class ArgumentParser:
    def __init__(self, ctx: FlowCtx):
        self.ctx = ctx

        self.schema = {}

        self.parsed_arguments = {}
        self.parsed_options = {}
        self.parsed_flags = {}

    def add_argument(self, name: str, help: str):
        if name in self.schema:
            raise DuplicateArgumentNameError(name)
        self.schema[name] = ArgumentSchema(name=name, help=help)

    def add_option(self, name: str, help: str, default: str):
        if name in self.schema:
            raise DuplicateArgumentNameError(name)
        self.schema[name] = OptionSchema(name=name, help=help, default=default)

    def add_flag(self, name: str, help: str):
        if name in self.schema:
            raise DuplicateArgumentNameError(name)
        self.schema[name] = FlagSchema(name=name, help=help)

    def _escape_name(self, x: str):
        return x.upper().replace("-", "_").replace(".", "_")

    def parse_args(self):
        for item in self.schema.values():
            if isinstance(item, ArgumentSchema):
                env_var = f"VARG_{self._escape_name(item.name)}"
                env_var_value = os.getenv(env_var)

                if env_var_value is None:  # Arguments are mandatory
                    raise ArgumentNotFoundError(item.name)

                self.parsed_arguments[item.name] = Argument(
                    name=item.name, value=env_var_value
                )

            elif isinstance(item, OptionSchema):
                env_var = f"VOPT_{self._escape_name(item.name)}"
                env_var_value = os.getenv(env_var) or item.default
                self.parsed_options[item.name] = Option(
                    name=item.name, value=env_var_value
                )

            elif isinstance(item, FlagSchema):
                env_var = f"VFLAG_{self._escape_name(item.name)}"
                env_var_value = os.getenv(env_var) or "0"
                self.parsed_flags[item.name] = Flag(
                    name=item.name, value=env_var_value == "1"
                )

    def context(self):
        """Return the list of parsed variables as a dict"""

        ctx_args = {x.name: x.value for x in self.parsed_arguments.values()}

        ctx_opts = {x.name: x.value for x in self.parsed_options.values()}

        ctx_flags = {x.name: x.value for x in self.parsed_flags.values()}

        return {**ctx_args, **ctx_opts, **ctx_flags}
