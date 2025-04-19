from verity.model.report import MethodReportLogItem, MethodReport
from verity.model.traceability import *
from verity.exchange import report_json

from datetime import datetime as dt

from uuid import uuid4


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


logs = [
    MethodReportLogItem(timestamp = dt.now(), severity="info", source="test", message="Hello world!"), 
    MethodReportLogItem(timestamp = dt.now(), severity="debug", source="test", message="This is test debug message"), 
]


test_report = MethodReport(
    uuid = str(uuid4()),
    date_started = dt.now(),
    date_ended   = dt.now(),
    environment = {
        "version": "1.0",
        "aaah": "bbbb",
    },

    context = {
        "what": "this",
    },
    traceability_graph = graph,
    logs = logs,
)

report_json.to_file(test_report, "output.json")
