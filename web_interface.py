from flask import Flask, render_template, request, send_file
from scanner import scan_url
import os

app = Flask(__name__)


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- START SCAN ----------------

@app.route("/scan", methods=["POST"])
def scan():

    url = request.form.get("url", "").strip()

    if not url:
        return {
            "success": False,
            "error": "Please enter a target URL."
        }

    # Run the scanner
    result = scan_url(url)

    return result


# ---------------- DOWNLOAD REPORT ----------------

@app.route("/download")
def download_report():

    filename = request.args.get("file", "")

    if not filename:
        return "No report specified.", 400

    # Prevent access outside the reports folder
    filename = os.path.basename(filename)

    filepath = os.path.join("reports", filename)

    if not os.path.exists(filepath):
        return "Report not found.", 404

    return send_file(
        filepath,
        as_attachment=True
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":


    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
