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
// CLEAR BUTTON
// ============================================================

clearButton.addEventListener("click", function () {

    codeInput.value = "";

    updateCharacterCount();

    resultsSection.classList.add("hidden");

    errorMessage.classList.add("hidden");

    predictionLabel.textContent = "-";

    confidenceValue.textContent = "0.00%";

    confidenceBar.style.width = "0%";

    issueCount.textContent = "0 Issues";

    issuesContainer.innerHTML = "";

    noIssues.classList.add("hidden");

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
// SHOW ERROR
// ============================================================

function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");
}


// ============================================================
// HIDE ERROR
// ============================================================

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

        const data = await response.json();

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

        showError(
            "Unable to analyze the code. " +
            error.message
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

    const confidence = Number(
        prediction.confidence || 0
    );


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

    confidenceValue.textContent =
        `${confidence.toFixed(2)}%`;


    // --------------------------------------------------------
    // CONFIDENCE PROGRESS BAR
    // --------------------------------------------------------

    const safeConfidence = Math.max(
        0,
        Math.min(100, confidence)
    );

    confidenceBar.style.width =
        `${safeConfidence}%`;


    // --------------------------------------------------------
    // STATIC ANALYSIS
    // --------------------------------------------------------

    const issues = Array.isArray(data.static_analysis)
        ? data.static_analysis
        : [];


    console.log(
        "Static analysis issues:",
        issues
    );


    displayStaticAnalysis(issues);
}


// ============================================================
// DISPLAY STATIC ANALYSIS
// ============================================================

function displayStaticAnalysis(issues) {

    // Clear old issues

    issuesContainer.innerHTML = "";


    // --------------------------------------------------------
    // ISSUE COUNT
    // --------------------------------------------------------

    issueCount.textContent =
        `${issues.length} ${issues.length === 1 ? "Issue" : "Issues"}`;


    // --------------------------------------------------------
    // NO ISSUES
    // --------------------------------------------------------

    if (issues.length === 0) {

        noIssues.classList.remove("hidden");

        return;
    }


    noIssues.classList.add("hidden");


    // --------------------------------------------------------
    // CREATE ISSUE CARDS
    // --------------------------------------------------------

    issues.forEach((issue, index) => {

        const issueCard =
            document.createElement("div");

        issueCard.className =
            "issue-item";


        // ----------------------------------------------------
        // ISSUE TYPE
        // ----------------------------------------------------

        const type =
            issue.type ||
            issue.title ||
            "Unknown Issue";


        // ----------------------------------------------------
        // ISSUE MESSAGE
        // ----------------------------------------------------

        const message =
            issue.message ||
            issue.description ||
            "No description available.";


        // ----------------------------------------------------
        // DETERMINE SEVERITY
        // ----------------------------------------------------

        let severity = "LOW";

        if (
            type.toLowerCase().includes("security") ||
            type.toLowerCase().includes("null") ||
            type.toLowerCase().includes("vulnerability")
        ) {

            severity = "MEDIUM";
        }


        // ----------------------------------------------------
        // CREATE HTML
        // ----------------------------------------------------

        issueCard.innerHTML = `

            <div class="issue-content">

                <div class="issue-top">

                    <h3>
                        ${escapeHtml(type)}
                    </h3>

                    <span class="severity ${severity.toLowerCase()}">
                        ${severity}
                    </span>

                </div>

                <p>
                    ${escapeHtml(message)}
                </p>

            </div>

        `;


        issuesContainer.appendChild(issueCard);

    });

}


// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHtml(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


// ============================================================
// START BACKEND CHECK
// ============================================================

checkBackend();


// ============================================================
// DEBUG
// ============================================================

console.log("Frontend JavaScript initialized.");