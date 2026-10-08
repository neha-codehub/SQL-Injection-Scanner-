import requests
import csv
import os
from datetime import datetime


ERROR_PATTERNS = [
    "sql syntax",
    "mysql",
    "warning",
    "postgresql",
    "ora-",
    "unclosed quotation mark",
    "sqlite"
]

PAYLOADS = [
    "'",
    '"'
]


def scan_url(url):
    """
    Scan a permitted target URL for basic SQL error indicators.
    Returns scan results for the web interface.
    """

    results = []
    logs = []

    if not url:
        return {
            "success": False,
            "error": "Target URL is required.",
            "results": [],
            "logs": []
        }

    url = url.strip()

    logs.append(f"> Target received: {url}")
    logs.append("> Initializing SQL injection detection...")
    logs.append(f"> Payloads loaded: {len(PAYLOADS)}")

    for payload in PAYLOADS:

        test_url = url + payload

        logs.append(f"> Testing payload: {repr(payload)}")

        try:
            response = requests.get(
                test_url,
                timeout=5
            )

            logs.append(
                f"> HTTP response received: {response.status_code}"
            )

            found = False

            for pattern in ERROR_PATTERNS:

                if pattern.lower() in response.text.lower():

                    logs.append(
                        f"> SQL error pattern detected: {pattern}"
                    )

                    results.append({
                        "url": test_url,
                        "payload": payload,
                        "pattern": pattern
                    })

                    found = True
                    break

            if not found:
                logs.append("> No SQL error pattern detected.")

        except requests.RequestException as e:

            logs.append(f"> Request error: {str(e)}")

    # Create reports directory
    os.makedirs("reports", exist_ok=True)

    filename = (
        f"reports/scan_report_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "URL",
            "Payload",
            "Matched Pattern"
        ])

        for result in results:
            writer.writerow([
                result["url"],
                result["payload"],
                result["pattern"]
            ])

    logs.append("> Scan completed.")
    logs.append(f"> Report saved: {filename}")

    return {
        "success": True,
        "results": results,
        "logs": logs,
        "payloads_tested": len(PAYLOADS),
        "issues_found": len(results),
        "report": filename
    }