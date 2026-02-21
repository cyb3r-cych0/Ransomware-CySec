import json
from datetime import datetime

def save_report(results, filename="scan_report.json"):
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": results
    }

    with open(filename, "w") as f:
        json.dump(report, f, indent=4)
