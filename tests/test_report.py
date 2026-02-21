from app.report import save_report
import os

def test_report_creation(tmp_path):
    file = tmp_path / "test_report.json"
    save_report([], filename=file)
    assert os.path.exists(file)
