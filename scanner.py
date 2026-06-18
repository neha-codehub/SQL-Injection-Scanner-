import requests
import csv
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

error_patterns = [
    "sql syntax",
    "mysql",
    "warning",
    "postgresql",
    "ora-",
    "unclosed quotation mark",
    "sqlite"
]

payloads = [
    "'",
    '"'
]

url = input("Enter target URL (with parameter): ")

print(Fore.CYAN + "\nStarting SQL Injection Detection...\n")

results = []

for payload in payloads:

    test_url = url + payload

    try:
        response = requests.get(test_url, timeout=5)

        found = False

        for pattern in error_patterns:

            if pattern.lower() in response.text.lower():

                print(Fore.RED + "[!] Possible SQL Error Detected")
                print(Fore.YELLOW + f"URL: {test_url}")
                print(Fore.GREEN + f"Matched Pattern: {pattern}\n")

                results.append([
                    test_url,
                    payload,
                    pattern
                ])

                found = True
                break

        if not found:
            print(Fore.GREEN + f"[SAFE] {test_url}")

    except Exception as e:
        print(Fore.RED + f"Request Error: {e}")

# Summary
print("\n" + "=" * 50)
print("SCAN SUMMARY")
print("=" * 50)

print(f"Payloads Tested : {len(payloads)}")
print(f"Issues Found    : {len(results)}")

# CSV Report
filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "URL",
        "Payload",
        "Matched Pattern"
    ])

    writer.writerows(results)

print(f"\nReport Saved: {filename}")
print("=" * 50)