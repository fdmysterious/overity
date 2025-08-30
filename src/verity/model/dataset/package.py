"""
Dataset package model
=====================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- August 2025
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from verity.model.dataset.metadata import DatasetMetadata


@dataclass
class DatasetPackageInfo:
    """Describes what is needed to build a dataset package"""

    """Dataset metadata information"""
    metadata: DatasetMetadata

    """Path to dataset path on local disk"""
    dataset_data_path: Path
