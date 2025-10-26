"""
Bench abstraction base class
============================

**June 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.

TODO: Parameters for base methods

"""

from __future__ import annotations
from abc import ABC, abstractmethod

from overity.model.ml_model.metadata import MLModelMetadata
from pathlib import Path


class BenchAbstraction(ABC):
    """
    Base class to define a bench abstraction
    """

    def __init__(self, settings: any):
        # TODO: Type annotation for bench settings?
        self.__configure__(settings)

    @property
    def capabilities(self) -> frozenset[str]:
        """Return the set of available capabilities"""
        return frozenset({})

    @property
    def compatible_tags(self) -> frozenset[str]:
        """Return the list of compatible execution targets tags"""
        return frozenset({})

    @property
    def compatible_targets(self) -> frozenset[str]:
        """Return the list of compatible execution targets slugs"""
        return frozenset({})

    @abstractmethod
    def __configure__(self, settings):
        """This method is implemented in children classes to configure the bench, given input settings"""
        pass

    @abstractmethod
    def bench_start(self):
        """Called to start bench (open connections, etc.)"""
        pass

    @abstractmethod
    def bench_cleanup(self):
        """Called to stop bench (close connections, remove temp files, etc.)"""
        pass

    @abstractmethod
    def sanity_check(self):
        """Called to check that bench is working OK"""

    @abstractmethod
    def state_initial(self):
        """Called to set bench to initial status"""

    @abstractmethod
    def state_panic(self):
        """Called for emergency bench stop"""

    # @abstractmethod
    # def agent_infos(self):
    #    """Get infos of used inference agent"""

    @abstractmethod
    def agent_deploy(self, model_file: Path, model_data: MLModelMetadata):
        """Called to deploy inference agent"""

    @abstractmethod
    def agent_start(self):
        """Called to start deployed inference agent"""

    @abstractmethod
    def agent_hello(self):
        """Called to test communication channel between bench and agent"""

    @abstractmethod
    def agent_inference(self, vectors: dict[str, any]):
        """Called to run an inference on the inference agent"""

    def has_capability(self, capability_name: str) -> bool:
        return capability_name in self.capabilities
