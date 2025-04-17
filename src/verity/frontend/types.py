"""
Utility types for frontend
==========================

- Florian Dupeyron (florian.dupeyron@elsys-design.com)
- April 2025
"""

from argparse import ArgumentError

from verity.model.general_info.method import MethodKind


def parse_method_kind(x: str):
    """Parse method kind from string argument."""

    # Training optimization
    if x in {"training-optimization", "to"}:
        return MethodKind.TrainingOptimization

    elif x in {"measurement-qualification", "mq"}:
        return MethodKind.MeasurementQualification

    elif x in {"deployment", "dp"}:
        return MethodKind.Deployment

    elif x in {"analysis", "an"}:
        return MethodKind.Analysis

    else:
        raise ArgumentError(x)
