from verity.model.traceability import *
from pprint import pprint

art_model      = ArtifactKey(kind = ArtifactKind.Model,                      id="my_model")
art_opt_report = ArtifactKey(kind = ArtifactKind.OptimizationReport,         id="aaaa-bbbb-cccc-dddd")
art_opt_run    = ArtifactKey(kind = ArtifactKind.OptimizationRun,            id="1111-2222-3333-4444")
art_dataset    = ArtifactKey(kind = ArtifactKind.Dataset,                    id="my_dataset")
art_topt_mtd   = ArtifactKey(kind = ArtifactKind.TrainingOptimizationMethod, id="my_method")

graph = ArtifactGraph()

graph.add(ArtifactLink(a=art_model, b=art_opt_run, kind=ArtifactLinkKind.ModelGeneratedBy))
graph.add(ArtifactLink(a=art_opt_report, b=art_opt_run, kind=ArtifactLinkKind.ReportFor))
graph.add(ArtifactLink(a=art_opt_run, b=art_dataset, kind=ArtifactLinkKind.DatasetUse))
graph.add(ArtifactLink(a=art_opt_run, b=art_topt_mtd, kind=ArtifactLinkKind.MethodUse))

def name_clean(x):
    return x.lower().replace("-","_")

print("graph TD")
for nd in graph.nodes:
    print(f"    {name_clean(nd.kind.value)}_{name_clean(nd.id)}[\"{nd.id} ({nd.kind.value})\"]")

for lk in graph.links:
    a_id = f"{name_clean(lk.a.kind.value)}_{name_clean(lk.a.id)}"
    b_id = f"{name_clean(lk.b.kind.value)}_{name_clean(lk.b.id)}"

    print(f"    {a_id} -->|{lk.kind.value}| {b_id}")
