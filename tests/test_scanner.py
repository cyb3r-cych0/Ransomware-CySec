from app.scanner import RansomwareScanner

def test_scan_structure():
    scanner = RansomwareScanner()
    result = scanner.scan("https://example.com")

    assert "url" in result
    assert "risk_score" in result
    assert isinstance(result["risk_score"], int)
