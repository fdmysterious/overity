from verity.exchange import report_json
from verity.backend.report_view import topt_html

from pathlib import Path

if __name__ == "__main__":
    report_path = Path("test_report.json")
    report_data = report_json.from_file(report_path)

    with open("output.html", "w") as fhandle:
        fhandle.write(topt_html.render(report_data, report_path))
        print("Output OK to output.html")
