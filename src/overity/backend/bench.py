"""
Overity.ai bench management backend features
============================================

**September 2025**

- Florian Dupeyron (florian.dupeyron@elsys-design.com)

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.
"""

import logging

from pathlib import Path

from overity.storage.local import LocalStorage
from overity.errors import InvalidBenchSettingsError, BenchInstanciationError

log = logging.getLogger("backend.bench")


def list_benches(program_path: Path):
    """List available bench instanciations in program"""

    program_path = Path(program_path)

    log.info(f"List bench instanciations from program {program_path}")
    st = LocalStorage(program_path)

    benches, errors = st.benches()

    return benches, errors


def list_bench_abstractions(program_path: Path):
    """List available bench abstractions in program"""

    program_path = Path(program_path)

    log.info(f"List bench abstractions from program {program_path}")
    st = LocalStorage(program_path)

    abstractions, errors = st.bench_abstractions()

    return abstractions, errors


def instanciate(program_path: Path, bench_slug: str):
    # Load program information
    program_path = Path(program_path)
    st = LocalStorage(program_path)

    # Import bench metadata
    bench = st.bench_load_infos(bench_slug)
    log.info(
        f"Instanciate bench '{bench.display_name}' ({bench.slug}) from {bench.abstraction_slug}"
    )

    # Import bench definitions
    BenchSettings, BenchDefinition = st.bench_abstraction_import_definitions(
        bench.abstraction_slug
    )

    # Parse bench settings
    try:
        bench_settings = BenchSettings(**bench.settings)
    except Exception as exc:
        raise InvalidBenchSettingsError(bench_slug, bench.settings, exc)

    # Instanciate bench
    try:
        bench_instance = BenchDefinition(bench_settings)
    except Exception as exc:
        raise BenchInstanciationError(bench_slug, bench.settings, exc)

    return bench_instance
