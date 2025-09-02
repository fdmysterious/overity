"""
Model definition for ML model packages
======================================

**December 2024**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from overity.model.ml_model.metadata import MLModelMetadata


@dataclass
class MLModelPackage:
    """Describes properties for a ML model package"""

    """ML Model metadata information"""
    metadata: MLModelMetadata

    """Path to input model file on local disk"""
    model_file_path: Path

    """Path to example implementation folder on local disk"""
    example_implementation_path: Optional[Path] = None
