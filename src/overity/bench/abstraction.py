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

from abc import ABC, abstractmethod
from overity.model.general_info.bench import BenchAbstractionMetadata


class BenchAbstraction(ABC):
    def __init__():
        pass

    @abstractmethod
    def metadata(self) -> BenchAbstractionMetadata:
        """Called to get bench abstraction metadata information"""

    @abstractmethod
    def sanity_check(self):
        """Called to check that bench is working OK"""

    @abstractmethod
    def initial_state(self):
        """Called to set bench to initial status"""

    @abstractmethod
    def agent_deploy(self):
        """Called to deploy inference agent"""

    @abstractmethod
    def agent_start(self):
        """Called to start deployed inference agent"""

    @abstractmethod
    def agent_hello(self):
        """Called to test communication channel between bench and agent"""

    @abstractmethod
    def agent_inference(self):
        """Called to run an inference on the inference agent"""

    @abstractmethod
    def panic(self):
        """Called to stop bench in urgence"""
