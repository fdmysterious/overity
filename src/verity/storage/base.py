"""
# Storage backend base class

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- February 2025
"""

import uuid
from abc import ABC, abstractmethod
from typing import Callable


class StorageBackend(ABC):

    # -------------------------- Catalyst

    @abstractmethod
    def program_info(self):
        """Get program information"""
        pass


    @abstractmethod
    def execution_targets(self):
        """Get list of execution targets registered in program"""
        pass

    

    # -------------------------- Ingredients

    @abstractmethod
    def training_optimization_methods(self):
        """Get list of optimization methods registered in program"""
        pass


    @abstractmethod
    def measurement_qualification_methods(self):
        """Get list of measurement and qualification methods registered in program"""
        pass


    @abstractmethod
    def deployment_methods(self):
        """Get list of deployment methods registered in program"""
        pass


    @abstractmethod
    def analysis_methods(self):
        """Get list of analysis methods registered in program"""
        pass


    @abstractmethod
    def experiments(self):
        """Get list of experiments definitions registered in program"""
        pass
    


    # -------------------------- Shelf

    @abstractmethod
    def experiment_runs(self):
        """Get list of experiment runs reports in program"""
        pass


    @abstractmethod
    def optimization_reports(self):
        """Get list of optimization reports in program"""
        pass


    @abstractmethod
    def execution_reports(self):
        """Get list of execution reports in program"""
        pass


    @abstractmethod
    def analysis_reports(self):
        """Get list of analysis reports in program"""
        pass


    # -------------------------- Precipitates

    @abstractmethod
    def models(self):
        """Get list of available models in program"""
        pass


    @abstractmethod
    def datasets(self):
        """Get list of available datasets in program"""
        pass



    # -------------------------- Generate IDs
    
    def _default_uuid_get(self, exists_fkt: Callable[[str], bool]):
        """Default UUID generation for a report. Generate the ID and check if it is available"""
        id = None
        while True:
            id = uuid.uuid4()
            if not exists_fkt(id):
                break

        return id


    def experiment_run_uuid_get(self):
        """Get an available run uuid"""
        return self._default_uuid_get(self.experiment_run_uuid_exists)


    def optimization_report_uuid_get(self):
        """Get an available optimization report uuid"""
        return self._default_uuid_get(self.optimization_report_uuid_exists)


    def execution_report_uuid_get(self):
        """Get an available execution report uuid"""
        return self._default_uuid_get(self.execution_report_uuid_exists)


    def analysis_report_uuid_get(self):
        """Get an available analysis report uuid"""
        return self._default_uuid_get(self.analysis_report_uuid_exists)


    # -------------------------- Check for IDs

    @abstractmethod
    def experiment_run_uuid_exists(self, run_uuid: str):
        """Check if the given uuid exists in experiment run reports"""
        pass

    @abstractmethod
    def optimization_report_uuid_exists(self, report_uuid: str):
        """Check if the given optimization report exists with given uuid"""
        pass

    @abstractmethod
    def execution_report_uuid_exists(self, report_uuid: str):
        """Check if the given execution report exists with given uuid"""
        pass

    @abstractmethod
    def analysis_report_uuid_exists(self, report_uuid: str):
        """Check if the given analysis report exists with given uuid"""
        pass
