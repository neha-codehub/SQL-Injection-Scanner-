# SQL Injection Detection Tool

This is a simple Python project that I built to learn about SQL Injection vulnerabilities and basic web security testing.

The tool sends different test inputs (payloads) to a target URL and checks the response for common database error messages. If a possible SQL-related error is found, it reports the issue and saves the results in a CSV file.

## Features

* Test multiple SQL Injection payloads
* Detect common SQL error patterns
* Display scan results in the terminal
* Generate a CSV report
* Works with a local vulnerable test application

## Technologies Used

* Python
* Requests
* Colorama
* CSV Module
* Flask (for local testing)

## Project Structure

sql_injection_scanner/

* scanner.py
* demo_app.py
* requirements.txt
* README.md

## How to Run

1. Install the required packages:

pip install -r requirements.txt

2. Start the demo application:

python demo_app.py

3. Open another terminal and run:

python scanner.py

4. Enter the target URL:

http://127.0.0.1:5000/product?id=

## Example Output

Possible SQL Error Detected

Matched Pattern: sql syntax

Report Saved: scan_report.csv

## What I Learned

While building this project, I learned:

* How HTTP requests work in Python
* Basic concepts of SQL Injection
* Response analysis and error detection
* CSV report generation
* Creating a simple security testing tool

## Note

This project was created for educational purposes and testing in controlled environments only.