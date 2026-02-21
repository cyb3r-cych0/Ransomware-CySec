import requests
from app.entropy import calculate_entropy

SUSPICIOUS_KEYWORDS = [
    "your files are encrypted",
    "pay in bitcoin",
    "decrypt",
    "ransom",
    ".locked",
    ".encrypted"
]

class RansomwareScanner:

    def scan(self, url):
        score = 0

        result = {
            "url": url,
            "keyword_detected": False,
            "high_entropy": False,
            "risk_score": 0
        }

        try:
            response = requests.get(url, timeout=5)
            content = response.text.lower()

            # Keyword detection
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword in content:
                    result["keyword_detected"] = True
                    score += 50
                    break

            # Entropy detection
            if "application" in response.headers.get("Content-Type", ""):
                entropy = calculate_entropy(response.content)
                if entropy > 7.5:
                    result["high_entropy"] = True
                    score += 50

        except:
            score += 10  # unreachable pages slightly suspicious

        result["risk_score"] = score
        return result
