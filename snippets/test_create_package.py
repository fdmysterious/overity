from pathlib import Path

from verity.exchange.model_package_v1 import package
from verity.model.ml_model.metadata import MLModelAuthor, MLModelMaintainer, MLModelMetadata
from verity.model.ml_model.package import MLModelPackage

cwd = (Path(__file__) / ".." ).resolve()


# Create model metadata
model_metadata = MLModelMetadata(
    name="SRU_binary_model_pruned_15_97",
    version="v0.1",
    authors = [
        MLModelAuthor(name="Samy Chehade", email="samy.chehade@elsys-design.com", contribution="Model training and adjustmeent"),
        MLModelAuthor(name="Adrien Tirlemont", email="adrien.tirlemont@avisto.com", contribution="Model architecture and initial training")
    ],

    maintainers = [
        MLModelMaintainer(name="Florian Dupeyron", email="florian.dupeyron@elsys-design.com"),
    ],

    target="agnostic",
    model_file="model.keras",
    exchange_format="keras",
)

model_file_path = cwd / "resources" / "SRU_binary_model_pruned_15_97_V2.keras"

model_package = MLModelPackage(
    metadata = model_metadata,
    model_file_path = model_file_path
)

#################################

archive_file_name = f"{model_metadata.name.lower()}-{model_metadata.version.replace('.', '_')}.tar.gz"

# Generate output archive
package.package_archive_create(model_package, cwd / archive_file_name)
