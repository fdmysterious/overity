"""
 # Local storage implementation

 - Florian Dupeyron (florian.dupeyron@elsys-design.com)
 - February 2025
 """

import logging
import traceback

from pathlib import Path
from ..base import StorageBackend

from verity.exchange import program_toml
from verity.exchange import execution_target_toml

log = logging.getLogger("Local storage")


class LocalStorage(StorageBackend):
    def __init__(self, folder: Path):
        self.base_folder = folder.resolve()


        # Initialize sub folders
        self.catalyst_folder                  = self.base_folder / "catalyst"
        self.ingredients_folder               = self.base_folder / "ingredients"
        self.shelf_folder                     = self.base_folder / "shelf"
        self.precipitates_folder              = self.base_folder / "precipitates"

        self.execution_targets_folder         = self.catalyst_folder / "execution_targets"

        self.training_optimization_folder     = self.ingredients_folder / "training_optimization"
        self.measurement_qualification_folder = self.ingredients_folder / "measurement_qualification"
        self.deployment_folder                = self.ingredients_folder / "deployment"
        self.analysis_folder                  = self.ingredients_folder / "analysis"
        self.experiments_folder               = self.ingredients_folder / "experiments"

        self.experiment_runs_folder           = self.shelf_folder / "experiment_runs"
        self.optimization_reports_folder      = self.shelf_folder / "optimization_reports"
        self.execution_reports_folder         = self.shelf_folder / "execution_reports"
        self.analysis_reports_folder          = self.shelf_folder / "analysis_reports"

        self.models_folder                    = self.precipitates_folder / "models"
        self.datasets_folder                  = self.precipitates_folder / "datasets"

        # Leaf folders are deepest folders that we use
        self.leaf_folders = [
            self.execution_targets_folder,
            self.training_optimization_folder,
            self.measurement_qualification_folder,
            self.deployment_folder,
            self.analysis_folder,
            self.experiments_folder,
            self.experiment_runs_folder,
            self.optimization_reports_folder,
            self.execution_reports_folder,
            self.analysis_reports_folder,
            self.experiment_runs_folder,
            self.optimization_reports_folder,
            self.execution_reports_folder,
            self.analysis_reports_folder,
            self.models_folder,
            self.datasets_folder,
        ]

        # Various path
        self.program_info_path = self.base_folder / "program.toml"


    def initialize(self):
        """Ensure folder exists and are writeable"""

        log.info(f"Initialize local storage in {self.base_folder!s}")

        for folder in self.leaf_folders:
            log.debug(f"Ensure {folder!s} exists")
            folder.mkdir(parents=True, exist_ok=True)


    # -------------------------- Get file paths

    def _execution_target_path(self, slug: str):
        return self.execution_targets_folder / f"{slug}.toml"

    def _training_optimization_info_path(self, slug: str):
        return self.training_optimization_folder / slug / "info.toml"

    def _measurement_qualification_info_path(self, slug: str):
        return self.measurement_qualification_folder / slug / "info.toml"

    def _deployement_method_info_path(self, slug: str):
        return self.deployment_folder / slug / "info.toml"

    def _analysis_method_info_path(self, slug: str):
        return self.analysis_folder / slug / "info.toml"

    def _experiments_method_info_path(self, slug: str):
        return self.experiments_folder / slug / "info.toml"

    def _experiment_run_report_path(self, run_uuid: str):
        return self.experiment_runs_folder / f"{run_uuid}.zip"

    def _optimization_report_path(self, run_uuid: str):
        return self.optimization_reports_folder / f"{run_uuid}.zip"

    def _execution_report_path(self, run_uuid: str):
        return self.execution_reports_folder / f"{run_uuid}.zip"

    def _analysis_report_path(self, run_uuid: str):
        return self.analysis_reports_folder / f"{run_uuid}.zip"

    def _model_path(self, slug: str):
        return self.models_folder / f"{slug}.zip"

    def _dataset_path(self, slug: str):
        return self.models_folder / f"{slug}.zip"


    # -------------------------- Catalyst

    def program_info(self):
        """Get program information"""

        if not self.program_info_path.is_file():
            raise FileNotFoundError(f"{self.program_info_path} is not a valid file or is not readable")

        program_info = program_toml.from_file(self.program_info_path)

        return program_info


    def execution_targets(self):
        """Get list of execution targets registered in program as a generator"""


        log.debug(f"Get list of execution targets from {self.execution_targets_folder}")
        
        # List TOML files in execution target folder

        def process_file(path):
            log.debug(f"Check file {path}")

            try:
                extg = execution_target_toml.from_file(path)
                return extg

            except Exception as exc:
                log.debug(f"Error checking {path}: {exc!s}")
                log.debug(traceback.format_exc())

        ex_targets = map(process_file, self.execution_targets_folder.glob("**/*.toml"))

        return ex_targets


    # -------------------------- Ingredients

    def training_optimization_methods(self):
        """Get list of optimization methods registered in program"""
        raise NotImplementedError()


    def measurement_qualification_methods(self):
        """Get list of measurement and qualification methods registered in program"""
        raise NotImplementedError()


    def deployment_methods(self):
        """Get list of deployment methods registered in program"""
        raise NotImplementedError()


    def analysis_methods(self):
        """Get list of analysis methods registered in program"""
        raise NotImplementedError()


    def experiments(self):
        """Get list of experiments definitions registered in program"""
        raise NotImplementedError()
    


    # -------------------------- Shelf

    def experiment_runs(self):
        """Get list of experiment runs reports in program"""
        raise NotImplementedError()


    def optimization_reports(self):
        """Get list of optimization reports in program"""
        raise NotImplementedError()


    def execution_reports(self):
        """Get list of execution reports in program"""
        raise NotImplementedError()


    def analysis_reports(self):
        """Get list of analysis reports in program"""

        # List of execution reports is implemented as a list of zip files with a uuid4 name

        raise NotImplementedError()


    # -------------------------- Precipitates

    def models(self):
        """Get list of available models in program"""
        raise NotImplementedError()


    def datasets(self):
        """Get list of available datasets in program"""
        raise NotImplementedError()


    # -------------------------- Check for IDs

    def experiment_run_uuid_exists(self, run_uuid: str):
        """Check if the given uuid exists in experiment run reports"""

        return self._experiment_run_report_path(run_uuid).is_file()



    def optimization_report_uuid_exists(self, report_uuid: str):
        """Check if the given optimization report exists with given uuid"""

        return self._optimization_report_path(report_uuid).is_file()


    def execution_report_uuid_exists(self, report_uuid: str):
        """Check if the given execution report exists with given uuid"""

        return self._execution_report_path(report_uuid).is_file()


    def analysis_report_uuid_exists(self, report_uuid: str):
        """Check if the given analysis report exists with given uuid"""

        return self._analysis_report_path(report_uuid).is_file()

