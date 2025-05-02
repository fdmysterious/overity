from pathlib import Path
import tempfile

from verity.exchange.model_package_v1 import package as ml_package

cwd = (Path(__file__) / "..").resolve()

archive_path = cwd / "storage" / "precipitates" / "models" / "sru_binary_model_pruned_15_97-v0_1.tar.gz"


with tempfile.TemporaryFile() as tmpfile:
    pkginfo = ml_package.model_load(archive_path, tmpfile)

    print( "Model information:")
    print( "------------------")
    print(f"-> name:    {pkginfo.name}"   )
    print(f"-> version: {pkginfo.version}")
    print("")
