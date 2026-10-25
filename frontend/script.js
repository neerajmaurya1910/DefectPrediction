// ============================================================
// JAVA DEFECT PREDICTION - FRONTEND
// ============================================================

const API_BASE_URL = "http://127.0.0.1:8000";
const ANALYZE_URL = `${API_BASE_URL}/analyze`;
const HEALTH_URL = `${API_BASE_URL}/health`;

// ============================================================
// GET HTML ELEMENTS
// ============================================================

const codeInput = document.getElementById("codeInput");
const analyzeButton = document.getElementById("analyzeButton");
const clearButton = document.getElementById("clearButton");

const buttonText = document.getElementById("buttonText");
const loader = document.getElementById("loader");

const characterCount = document.getElementById("characterCount");

const apiStatus = document.getElementById("apiStatus");
const statusDot = document.getElementById("statusDot");

const errorMessage = document.getElementById("errorMessage");
const resultsSection = document.getElementById("resultsSection");

const predictionLabel = document.getElementById("predictionLabel");
const confidenceValue = document.getElementById("confidenceValue");
const confidenceBar = document.getElementById("confidenceBar");

const issueCount = document.getElementById("issueCount");
const issuesContainer = document.getElementById("issuesContainer");
const noIssues = document.getElementById("noIssues");


// ============================================================
// INITIALIZATION
// ============================================================

console.log("Java Defect Prediction Frontend Loaded.");
console.log("Backend:", API_BASE_URL);
console.log("Analyze URL:", ANALYZE_URL);


// ============================================================
// CHARACTER COUNT
// ============================================================

function updateCharacterCount() {
    const length = codeInput.value.length;
    characterCount.textContent = `${length} characters`;
}

codeInput.addEventListener("input", updateCharacterCount);

updateCharacterCount();


// ============================================================
// CLEAR / RESET RESULTS
// ============================================================
// Used both by the "Clear" button and right before a new
// analysis request is sent, so no result from a previous
// run is ever left on screen.

function clearResults() {

    predictionLabel.textContent = "-";

    confidenceValue.textContent = "0.00%";

    confidenceBar.style.width = "0%";

    issueCount.textContent = "0 Issues";

    // Remove all previously rendered issue cards
    while (issuesContainer.firstChild) {
        issuesContainer.removeChild(issuesContainer.firstChild);
    }

    noIssues.classList.add("hidden");
}

clearButton.addEventListener("click", function () {

    codeInput.value = "";

    updateCharacterCount();

    hideError();

    resultsSection.classList.add("hidden");

    clearResults();

    const acriScore = document.getElementById("acriScore");
    const acriPriority = document.getElementById("acriPriority");
    const acriBar = document.getElementById("acriBar");
    const acriExplanation = document.getElementById("acriExplanation");

    if (acriScore) acriScore.textContent = "- / 100";

    if (acriPriority) {
        acriPriority.textContent = "Awaiting analysis";
        acriPriority.className = "acri-priority";
    }

    if (acriBar) acriBar.style.width = "0%";

    if (acriExplanation) {
        acriExplanation.textContent = "Analyze Java code to calculate ACRI.";
    }

    const acriStatic = document.getElementById("acriStaticScore");
    const acriComplexity = document.getElementById("acriComplexityScore");
    const acriModel = document.getElementById("acriModelScore");

    if (acriStatic) acriStatic.textContent = "-";
    if (acriComplexity) acriComplexity.textContent = "-";
    if (acriModel) acriModel.textContent = "-";
});


// ============================================================
// CHECK BACKEND STATUS
// ============================================================

async function checkBackend() {

    console.log("Checking backend:", HEALTH_URL);

    try {

        const response = await fetch(HEALTH_URL);

        if (!response.ok) {
            throw new Error("Backend returned an error.");
        }

        const data = await response.json();

        console.log("Backend health response:", data);

        statusDot.classList.remove("offline");
        statusDot.classList.add("online");

        apiStatus.textContent = "API Online";

        console.log("Backend is online.");

    } catch (error) {

        console.error("Backend is offline:", error);

        statusDot.classList.remove("online");
        statusDot.classList.add("offline");

        apiStatus.textContent = "API Offline";
    }
}


// ============================================================
// SHOW / HIDE ERROR
// ============================================================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");
}

function hideError() {

    errorMessage.textContent = "";

    errorMessage.classList.add("hidden");
}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(isLoading) {

    if (isLoading) {

        analyzeButton.disabled = true;

        buttonText.textContent = "Analyzing...";

        loader.classList.remove("hidden");

    } else {

        analyzeButton.disabled = false;

        buttonText.textContent = "Analyze Code";

        loader.classList.add("hidden");
    }
}


// ============================================================
// ANALYZE BUTTON
// ============================================================

analyzeButton.addEventListener("click", analyzeCode);


// ============================================================
// MAIN ANALYZE FUNCTION
// ============================================================

async function analyzeCode() {

    hideError();

    const code = codeInput.value.trim();

    // --------------------------------------------------------
    // Validate input
    // --------------------------------------------------------

    if (!code) {
        showError("Please enter Java code before analyzing.");
        return;
    }

    console.log("==============================");
    console.log("Sending Java code to backend...");
    console.log("URL:", ANALYZE_URL);
    console.log("Code:", code);

    // --------------------------------------------------------
    // Reset/hide the previous result BEFORE sending the new
    // request, so nothing stale from the last run is visible
    // while we wait for the backend.
    // --------------------------------------------------------

    resultsSection.classList.add("hidden");
    clearResults();

    setLoading(true);

    try {

        // ----------------------------------------------------
        // SEND REQUEST TO BACKEND
        // ----------------------------------------------------

        const response = await fetch(ANALYZE_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                code: code
            })

        });

        console.log("HTTP Status:", response.status);

        // ----------------------------------------------------
        // GET RESPONSE
        // ----------------------------------------------------

        let data;

        try {
            data = await response.json();
        } catch (parseError) {
            throw new Error("Received an invalid response from the backend.");
        }

        console.log("==============================");
        console.log("BACKEND RESPONSE:");
        console.log(data);

        // ----------------------------------------------------
        // CHECK HTTP ERROR
        // ----------------------------------------------------

        if (!response.ok) {

            throw new Error(
                data.detail ||
                data.message ||
                "Backend returned an error."
            );
        }

        // ----------------------------------------------------
        // CHECK SUCCESS
        // ----------------------------------------------------

        if (data.success === false) {

            throw new Error(
                data.message ||
                "Analysis failed."
            );
        }

        // ----------------------------------------------------
        // DISPLAY BACKEND DATA
        // ----------------------------------------------------

        console.log("==============================");
        console.log("Displaying backend data:");

        displayResults(data);

    } catch (error) {

        console.error("==============================");
        console.error("ANALYSIS ERROR:");
        console.error(error);

        const isNetworkError = error instanceof TypeError;

        showError(
            isNetworkError
                ? `Unable to connect to the backend. Make sure FastAPI is running at ${API_BASE_URL}.`
                : "Unable to analyze the code. " + error.message
        );

    } finally {

        setLoading(false);
    }
}


// ============================================================
// DISPLAY COMPLETE RESULTS
// ============================================================

function displayResults(data) {

    console.log("Backend data received:", data);

    // --------------------------------------------------------
    // SHOW RESULTS SECTION
    // --------------------------------------------------------

    resultsSection.classList.remove("hidden");

    // --------------------------------------------------------
    // GET PREDICTION
    // --------------------------------------------------------

    const prediction = data.prediction || {};

    const label = prediction.label || "Unknown";

    let confidence = Number(prediction.confidence);

    if (!Number.isFinite(confidence)) {
        confidence = 0;
    }

    // The backend already returns confidence as a 0-100 percent
    // value (see predict_defect() in backend/app.py, which does
    // round(probability * 100, 2)). Only scale up if a backend
    // change ever starts returning a 0-1 decimal instead.
    if (confidence > 0 && confidence <= 1) {
        confidence = confidence * 100;
    }

    console.log("Prediction:", prediction);
    console.log("Label:", label);
    console.log("Confidence:", confidence);

    // --------------------------------------------------------
    // DISPLAY CWE LABEL
    // --------------------------------------------------------

    predictionLabel.textContent = label;

    // --------------------------------------------------------
    // DISPLAY CONFIDENCE
    // --------------------------------------------------------

    confidenceValue.textContent = `${confidence.toFixed(2)}%`;

    // --------------------------------------------------------
    // CONFIDENCE PROGRESS BAR
    // --------------------------------------------------------

    const safeConfidence = Math.max(0, Math.min(100, confidence));

    confidenceBar.style.width = `${safeConfidence}%`;

    // --------------------------------------------------------
    // STATIC ANALYSIS
    // --------------------------------------------------------

    const issues = Array.isArray(data.static_analysis)
        ? data.static_analysis
        : [];

    console.log("Static analysis issues:", issues);

    displayStaticAnalysis(issues);
    // Display software metrics
    displaySoftwareMetrics(data.software_metrics || {});
    displayACRI(data.acri);
}


// ============================================================
// DISPLAY STATIC ANALYSIS
// ============================================================


function displayStaticAnalysis(issues) {
    // Clear previous results
    while (issuesContainer.firstChild) {
        issuesContainer.removeChild(issuesContainer.firstChild);
    }

    // Update issue count
    issueCount.textContent =
        `${issues.length} ${issues.length === 1 ? "Issue" : "Issues"}`;

    // Show message when no issues are found
    if (issues.length === 0) {
        noIssues.classList.remove("hidden");
        return;
    }

    noIssues.classList.add("hidden");

    const KNOWN_SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

    issues.forEach((issue) => {
        const type = issue.type || issue.title || "Unknown Issue";
        const message =
            issue.message || issue.description || "No description available.";

        const severity =
            typeof issue.severity === "string" && issue.severity.trim()
                ? issue.severity.trim().toUpperCase()
                : "LOW";

        const severityClass = KNOWN_SEVERITIES.includes(severity)
            ? severity.toLowerCase()
            : "low";

        // Create issue card
        const issueCard = document.createElement("div");
        issueCard.className = "issue-item";

        const issueContent = document.createElement("div");
        issueContent.className = "issue-content";

        // Issue heading and severity badge
        const issueTop = document.createElement("div");
        issueTop.className = "issue-top";

        const typeHeading = document.createElement("h3");
        typeHeading.textContent = type;

        const severityBadge = document.createElement("span");
        severityBadge.className = `severity ${severityClass}`;
        severityBadge.textContent = severity;

        issueTop.appendChild(typeHeading);
        issueTop.appendChild(severityBadge);
        issueContent.appendChild(issueTop);

        // Issue explanation
        const messageParagraph = document.createElement("p");
        messageParagraph.textContent = message;
        issueContent.appendChild(messageParagraph);

        // NEW FEATURE: Display line number
        if (Number.isInteger(issue.line) && issue.line > 0) {
            const lineInfo = document.createElement("p");
            lineInfo.className = "issue-line";
            lineInfo.textContent = `Line: ${issue.line}`;
            issueContent.appendChild(lineInfo);
        }

        // NEW FEATURE: Display affected source code
        if (typeof issue.code === "string" && issue.code.trim()) {
            const codeBlock = document.createElement("pre");
            codeBlock.className = "issue-code";

            const codeText = document.createElement("code");
            codeText.textContent = issue.code;

            codeBlock.appendChild(codeText);
            issueContent.appendChild(codeBlock);
        }

        issueCard.appendChild(issueContent);
        issuesContainer.appendChild(issueCard);
    });
}


// ============================================================
// START BACKEND CHECK
// ============================================================

checkBackend();


// ============================================================
// DEBUG
// ============================================================

console.log("Frontend JavaScript initialized.");

function displaySoftwareMetrics(metrics) {
    const metricElements = {
        metricTotalLines: metrics.total_lines,
        metricLOC: metrics.loc,
        metricComplexity: metrics.cyclomatic_complexity_estimate,
        metricMethods: metrics.method_count,
        metricComments: metrics.comment_lines,
        metricCommentPercentage: metrics.comment_percentage
    };

    // Update each metric card safely
    Object.entries(metricElements).forEach(([id, value]) => {
        const element = document.getElementById(id);

        if (!element) {
            console.warn(`Metric element not found: ${id}`);
            return;
        }

        if (value === undefined || value === null) {
            element.textContent = "-";
        } else {
            element.textContent =
                id === "metricCommentPercentage"
                    ? `${Number(value).toFixed(2)}%`
                    : String(value);
        }
    });

    // Give a simple interpretation of the complexity estimate.
    // This is an illustrative threshold, not a universal standard.
    const complexityElement =
        document.getElementById("complexityLevel");

    if (complexityElement) {
        const complexity =
            Number(metrics.cyclomatic_complexity_estimate);

        if (!Number.isFinite(complexity) || complexity < 1) {
            complexityElement.textContent = "Unavailable";
        } else if (complexity <= 5) {
            complexityElement.textContent = "Low estimate";
        } else if (complexity <= 10) {
            complexityElement.textContent = "Moderate estimate";
        } else {
            complexityElement.textContent = "High estimate";
        }
    }
}


function displayACRI(acri) {
    const scoreElement = document.getElementById("acriScore");
    const priorityElement = document.getElementById("acriPriority");
    const barElement = document.getElementById("acriBar");
    const explanationElement = document.getElementById("acriExplanation");
    const staticElement = document.getElementById("acriStaticScore");
    const complexityElement = document.getElementById("acriComplexityScore");
    const modelElement = document.getElementById("acriModelScore");
    if (!acri || !Number.isFinite(Number(acri.score))) {
        if (scoreElement) scoreElement.textContent = "Unavailable";
        if (priorityElement) priorityElement.textContent = "-";
        if (barElement) barElement.style.width = "0%";
        if (explanationElement) {
            explanationElement.textContent = "ACRI was not returned by the backend.";
        }
        return;
    }

    const score = Math.max(0, Math.min(100, Number(acri.score)));

    if (scoreElement) {
        scoreElement.textContent = score.toFixed(2) + " / 100";
    }

    if (priorityElement) {
        const priority = acri.priority || "Unclassified";

        priorityElement.textContent = priority;
        priorityElement.className =
            "acri-priority acri-" + priority.toLowerCase();
    }

    if (barElement) {
        barElement.style.width = score + "%";
    }

    
    const components = acri.components || {};

    if (staticElement) {
        staticElement.textContent =
            Number(components.static_finding_severity_score ?? 0).toFixed(2);
    }

    if (complexityElement) {
        complexityElement.textContent =
            Number(components.complexity_risk ?? 0).toFixed(2);
    }

    if (modelElement) {
        modelElement.textContent =
            Number(components.model_signal ?? 0).toFixed(2);
    }


    if (explanationElement) {
        explanationElement.textContent =
            acri.explanation ||
            "This score combines static findings, complexity, and the AI model signal.";
    }
}
