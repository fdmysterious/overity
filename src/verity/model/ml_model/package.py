"""
# Model definition for ML model packages

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- December 2024
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from verity.model.ml_model.metadata import MLModelMetadata


@dataclass
class MLModelPackage:
    """Describes properties for a ML model package"""

    """ML Model metadata information"""
    metadata: MLModelMetadata

    """Path to input model file on local disk"""
    model_file_path: Path

    """Path to example implementation folder on local disk"""
    example_implementation_path: Optional[Path] = None
