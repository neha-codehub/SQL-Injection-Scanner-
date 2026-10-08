const scanForm = document.getElementById("scanForm");
const scanButton = document.getElementById("scanButton");

const terminalOutput = document.getElementById("terminalOutput");
const payloadCount = document.getElementById("payloadCount");
const issueCount = document.getElementById("issueCount");
const scanStatus = document.getElementById("scanStatus");

const resultsContainer = document.getElementById("results");

const reportSection = document.getElementById("reportSection");
const downloadReport = document.getElementById("downloadReport");


/* =========================
   TERMINAL LOG
========================= */

function addLog(message, type = "") {

    const line = document.createElement("p");

    if (type === "danger") {
        line.className = "log-danger";
    }

    if (type === "warning") {
        line.className = "log-warning";
    }

    if (type === "success") {
        line.className = "log-success";
    }

    const prompt = document.createElement("span");

    prompt.className = "prompt";
    prompt.textContent = "root@scanner:~$ ";

    line.appendChild(prompt);
    line.appendChild(document.createTextNode(message));

    terminalOutput.appendChild(line);

    terminalOutput.scrollTop =
        terminalOutput.scrollHeight;
}


/* =========================
   DISPLAY RESULTS
========================= */

function displayResults(results) {

    resultsContainer.innerHTML = "";

    if (!results || results.length === 0) {

        resultsContainer.innerHTML = `
            <div class="no-results">
                ✓ No SQL error indicators detected.
            </div>
        `;

        return;
    }

    results.forEach(function(result) {

        const card = document.createElement("div");
        card.className = "result-card";

        const title = document.createElement("div");
        title.className = "result-title";
        title.textContent =
            "⚠ POSSIBLE SQL ERROR INDICATOR";

        const urlRow = document.createElement("div");
        urlRow.className = "result-row";
        urlRow.innerHTML = "<strong>URL:</strong> ";
        urlRow.appendChild(
            document.createTextNode(result.url)
        );

        const payloadRow = document.createElement("div");
        payloadRow.className = "result-row";
        payloadRow.innerHTML = "<strong>Payload:</strong> ";
        payloadRow.appendChild(
            document.createTextNode(result.payload)
        );

        const patternRow = document.createElement("div");
        patternRow.className = "result-row";
        patternRow.innerHTML =
            "<strong>Matched Pattern:</strong> ";
        patternRow.appendChild(
            document.createTextNode(result.pattern)
        );

        card.appendChild(title);
        card.appendChild(urlRow);
        card.appendChild(payloadRow);
        card.appendChild(patternRow);

        resultsContainer.appendChild(card);

    });
}


/* =========================
   START SCAN
========================= */

scanForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const url =
        document.getElementById("url").value.trim();

    if (!url) {

        alert("Please enter a target URL.");

        return;
    }


    /* RESET */

    terminalOutput.innerHTML = "";

    resultsContainer.innerHTML = `
        <div class="no-results">
            Scanning target...
        </div>
    `;

    payloadCount.textContent = "0";
    issueCount.textContent = "0";
    scanStatus.textContent = "SCANNING";

    reportSection.style.display = "none";

    scanButton.disabled = true;
    scanButton.innerHTML = "⟳ SCANNING...";


    addLog("Target received: " + url);
    addLog("Initializing SQL injection detection...");


    try {

        const formData = new FormData();

        formData.append("url", url);


        const response = await fetch("/scan", {
            method: "POST",
            body: formData
        });


        if (!response.ok) {

            throw new Error(
                "Server returned HTTP " +
                response.status
            );

        }


        const data = await response.json();


        /* SERVER ERROR */

        if (!data.success) {

            addLog(
                data.error || "Scan failed.",
                "danger"
            );

            scanStatus.textContent = "ERROR";

            return;
        }


        /* DISPLAY SERVER LOGS */

        terminalOutput.innerHTML = "";

        if (data.logs) {

            data.logs.forEach(function(log) {

                let type = "";

                const lower = log.toLowerCase();

                if (
                    lower.includes("error pattern") ||
                    lower.includes("detected")
                ) {

                    type = "danger";

                }
                else if (
                    lower.includes("completed") ||
                    lower.includes("saved")
                ) {

                    type = "success";

                }

                addLog(log, type);

            });

        }


        /* STATISTICS */

        payloadCount.textContent =
            data.payloads_tested || 0;

        issueCount.textContent =
            data.issues_found || 0;


        if (data.issues_found > 0) {

            scanStatus.textContent =
                "ISSUES FOUND";

        }
        else {

            scanStatus.textContent =
                "COMPLETED";

        }


        /* RESULTS */

        displayResults(data.results);


        /* CSV REPORT */

        if (data.report) {

            const filename =
                data.report.split(/[\\/]/).pop();

            downloadReport.href =
                "/download?file=" +
                encodeURIComponent(filename);

            reportSection.style.display = "block";
        }

    }

    catch (error) {

        console.error(error);

        addLog(
            "Connection error: " +
            error.message,
            "danger"
        );

        scanStatus.textContent = "ERROR";

    }

    finally {

        scanButton.disabled = false;

        scanButton.innerHTML =
            "<span>▶</span> START SCAN";

    }

});