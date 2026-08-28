Absolutely. Below is a **complete, detailed `README.md`** you can paste directly into your project. It is written for your **Java Defect Prediction / Java Code Security Analyzer** project, including the **FastAPI backend, CodeBERT prediction, static analysis, frontend, API communication, setup, testing, troubleshooting, and project structure**.

````markdown
# Java Defect Prediction System

## Java Code Security Analyzer

A web-based Java source-code analysis system that combines **Static Analysis** and a **CodeBERT-based Machine Learning model** to detect potential vulnerabilities and code-quality issues in Java programs.

The system allows a user to paste Java source code into a web interface and receive an analysis from a Python FastAPI backend.

The backend performs two major tasks:

1. **Static Analysis**
   - Searches for potentially dangerous or poor coding patterns.
   - Reports detected issues with type, message, and severity.

2. **AI-Based Vulnerability Prediction**
   - Uses a CodeBERT-based model to predict whether the submitted Java code is associated with a vulnerability.
   - Returns a predicted CWE label and confidence score.

The frontend receives the backend response using JavaScript and dynamically displays the results.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [How the System Works](#how-the-system-works)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Installation](#installation)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Analyze API](#analyze-api)
- [Health Check API](#health-check-api)
- [Backend Response Format](#backend-response-format)
- [Frontend and Backend Communication](#frontend-and-backend-communication)
- [AI Prediction](#ai-prediction)
- [Static Analysis](#static-analysis)
- [Testing the Application](#testing-the-application)
- [Example Java Code](#example-java-code)
- [Expected Results](#expected-results)
- [Testing Different Java Programs](#testing-different-java-programs)
- [Troubleshooting](#troubleshooting)
- [Common Errors](#common-errors)
- [Development Workflow](#development-workflow)
- [Future Improvements](#future-improvements)
- [Limitations](#limitations)
- [Security Considerations](#security-considerations)
- [Conclusion](#conclusion)

---

# Project Overview

The Java Defect Prediction System is designed to analyze Java source code and provide developers with information about possible defects, vulnerabilities, and code-quality problems.

The project contains a frontend and backend.

### Frontend

The frontend provides a web interface where the user can:

- Enter Java source code.
- Clear the code editor.
- Submit the code for analysis.
- View API status.
- View the predicted vulnerability.
- View the model confidence.
- View static analysis issues.
- View issue severity.

### Backend

The backend is implemented using FastAPI.

It receives Java source code from the frontend through an HTTP request.

The backend then:

1. Validates the request.
2. Performs static analysis.
3. Sends the source code to the CodeBERT model.
4. Generates a vulnerability prediction.
5. Calculates the confidence score.
6. Combines the results.
7. Returns a JSON response to the frontend.

---

# Features

## 1. Java Source Code Input

Users can paste Java code into the source-code editor.

Example:

```java
public class Test {

    public static void main(String[] args) {

        String input = null;

        System.out.println(input.length());
    }
}
````

---

## 2. Static Analysis

The backend checks the Java source code for predefined problematic patterns.

Examples include:

* Null safety problems.
* Unsafe object usage.
* Poor logging practices.
* Potential security issues.
* Other code-quality patterns implemented in the backend.

Each issue contains information such as:

* Issue type.
* Description/message.
* Severity.

---

## 3. AI Vulnerability Prediction

The application uses a CodeBERT-based model for vulnerability prediction.

The prediction contains:

* Vulnerability label.
* Confidence score.

Example:

```json
{
    "label": "CWE-78",
    "confidence": 33.37
}
```

---

## 4. Dynamic Frontend Results

The frontend does not use hardcoded analysis results.

After the user clicks:

```text
Analyze Code
```

the JavaScript frontend sends the code to:

```text
http://127.0.0.1:8000/analyze
```

The backend processes the request and sends a JSON response.

The frontend then dynamically updates:

* Predicted Vulnerability.
* Confidence.
* Confidence progress bar.
* Number of static-analysis issues.
* Issue descriptions.
* Severity.

---

## 5. Backend Health Check

The frontend checks whether the backend is running.

Health endpoint:

```text
http://127.0.0.1:8000/health
```

If the backend is available, the frontend displays:

```text
API Online
```

---

# System Architecture

The application follows a client-server architecture.

```text
                    USER
                     |
                     |
                     v
             +---------------+
             |   FRONTEND    |
             |               |
             |   HTML        |
             |   CSS         |
             |   JavaScript  |
             +-------+-------+
                     |
                     | HTTP POST
                     | /analyze
                     v
             +---------------+
             |    FASTAPI    |
             |    BACKEND    |
             +-------+-------+
                     |
             +-------+-------+
             |               |
             v               v
      +-------------+   +-------------+
      |   Static    |   |   CodeBERT  |
      |   Analysis  |   |    Model    |
      +------+------+   +------+------+
             |                 |
             +--------+--------+
                      |
                      v
                JSON Response
                      |
                      v
             +---------------+
             |   FRONTEND    |
             |   JavaScript   |
             +-------+-------+
                     |
                     v
              Display Results
```

---

# How the System Works

The complete workflow is:

```text
1. User opens frontend
        |
        v
2. Frontend checks /health
        |
        v
3. Backend responds
        |
        v
4. User enters Java code
        |
        v
5. User clicks "Analyze Code"
        |
        v
6. JavaScript sends POST /analyze
        |
        v
7. FastAPI receives Java code
        |
        v
8. Static analysis is performed
        |
        v
9. CodeBERT predicts vulnerability
        |
        v
10. Backend creates JSON response
        |
        v
11. Frontend receives JSON
        |
        v
12. JavaScript extracts prediction
        |
        v
13. JavaScript extracts static analysis
        |
        v
14. UI is updated
```

---

# Project Structure

The project is organized approximately as follows:

```text
DefectPrediction/
│
├── backend/
│   │
│   ├── app.py
│   ├── dataset/
│   └── __pycache__/
│
├── frontend/
│   │
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── models/
│
├── notebooks/
│
├── results/
│
├── src/
│
├── train_codebert.py
├── static_analysis.py
├── eda.py
├── extract_dataset.py
│
├── .gitignore
│
└── README.md
```

The exact structure may vary depending on the current development version of the project.

---

# Technologies Used

## Frontend

### HTML

Used to create the structure of the web application.

### CSS

Used to design:

* Cards.
* Buttons.
* Forms.
* Progress bars.
* Status indicators.
* Issue containers.

### JavaScript

Used for:

* Sending API requests.
* Receiving backend responses.
* Updating the user interface.
* Handling errors.
* Checking backend status.
* Displaying analysis results.

---

# Backend

## Python

Python is used for the backend and machine-learning components.

## FastAPI

FastAPI provides the REST API.

## Uvicorn

Uvicorn is used to run the FastAPI application.

## Transformers

The Hugging Face Transformers library is used for CodeBERT.

## PyTorch

PyTorch is used by the machine-learning model.

---

# Machine Learning

The project uses CodeBERT for source-code understanding and vulnerability prediction.

CodeBERT is a transformer-based model designed to understand programming languages and natural language.

The model is used to analyze Java source code and generate a vulnerability prediction.

---

# Requirements

Before running the project, install the following:

* Python 3.9 or newer
* pip
* A modern web browser
* VS Code or another code editor
* Git (optional)

Python packages may include:

```text
fastapi
uvicorn
transformers
torch
numpy
pandas
scikit-learn
```

Additional dependencies may be required depending on the current implementation.

---

# Installation

## Step 1: Clone or Extract the Project

If using Git:

```bash
git clone <repository-url>
```

Then enter the project:

```bash
cd DefectPrediction
```

If the project was provided as a ZIP file, extract the ZIP file and open the extracted folder in VS Code.

---

# Backend Setup

Open a terminal in the project directory.

Move to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# Install Dependencies

Install the required packages:

```bash
pip install fastapi uvicorn transformers torch pandas numpy scikit-learn
```

If the project contains a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

---

# Running the Backend

From the project root:

```bash
uvicorn backend.app:app --reload
```

Or, if you are inside the backend directory:

```bash
uvicorn app:app --reload
```

The backend should start at:

```text
http://127.0.0.1:8000
```

You should see something similar to:

```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

# Backend Health Check

Open the following URL in your browser:

```text
http://127.0.0.1:8000/health
```

The backend should return a response indicating that the API is running.

For example:

```json
{
    "status": "ok"
}
```

The exact response depends on the implementation in `app.py`.

---

# FastAPI Documentation

FastAPI automatically provides API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

This provides an interactive Swagger UI.

You can use it to test the backend without the frontend.

---

# Frontend Setup

The frontend is located inside:

```text
frontend/
```

Important files:

```text
frontend/index.html
frontend/script.js
frontend/style.css
```

---

# Running the Frontend

The frontend can be opened using VS Code Live Server.

Open:

```text
frontend/index.html
```

Then click:

```text
Go Live
```

The frontend may open at something similar to:

```text
http://127.0.0.1:5501/frontend/index.html
```

The exact port may be different.

---

# Important

The frontend and backend are two separate services.

### Frontend

Example:

```text
http://127.0.0.1:5501
```

### Backend

Example:

```text
http://127.0.0.1:8000
```

Both must be running.

---

# Running the Complete Application

You should have two terminals.

## Terminal 1 - Backend

```bash
uvicorn backend.app:app --reload
```

The backend runs on:

```text
http://127.0.0.1:8000
```

---

## Terminal 2 - Frontend

Start Live Server from VS Code.

The frontend runs on something similar to:

```text
http://127.0.0.1:5501
```

---

# API Endpoints

The main API endpoints are:

```text
GET  /health
POST /analyze
```

---

# Health Check API

## Endpoint

```text
GET /health
```

Purpose:

Checks whether the backend is running.

Example:

```text
http://127.0.0.1:8000/health
```

---

# Analyze API

## Endpoint

```text
POST /analyze
```

Purpose:

Analyzes Java source code.

The frontend sends Java source code to this endpoint.

---

# Analyze Request

The request should contain the Java source code.

Example:

```json
{
    "code": "public class Test { public static void main(String[] args) { System.out.println(\"Hello\"); } }"
}
```

The exact request property must match the request model implemented in `backend/app.py`.

---

# Analyze Response

A successful response has the following general structure:

```json
{
    "success": true,
    "prediction": {
        "label": "CWE-78",
        "confidence": 33.37
    },
    "static_analysis": [
        {
            "type": "Null Safety",
            "message": "Object method is called without an obvious null check.",
            "severity": "MEDIUM"
        },
        {
            "type": "Code Quality",
            "message": "System.out.println found. Consider using a logging framework.",
            "severity": "LOW"
        }
    ]
}
```

The exact values depend on the submitted Java code and the model.

---

# Backend Response Format

The frontend expects the backend response to contain:

```text
success
prediction
static_analysis
```

The prediction object contains:

```text
label
confidence
```

The static analysis array contains individual issues.

Each issue may contain:

```text
type
message
severity
```

---

# Frontend and Backend Communication

The JavaScript frontend sends the source code using the Fetch API.

The basic communication pattern is:

```javascript
const response = await fetch(
    "http://127.0.0.1:8000/analyze",
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            code: code
        })
    }
);
```

Then the response is converted into JSON:

```javascript
const data = await response.json();
```

The frontend then extracts:

```javascript
data.prediction
```

and:

```javascript
data.static_analysis
```

and displays them in the UI.

---

# CORS

Because the frontend and backend run on different ports, the browser considers them different origins.

For example:

```text
Frontend:
http://127.0.0.1:5501
```

and:

```text
Backend:
http://127.0.0.1:8000
```

Therefore, the FastAPI backend should allow the frontend origin through CORS.

A typical FastAPI configuration is:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production deployment, it is better to restrict `allow_origins` to trusted frontend domains.

---

# AI Prediction

The CodeBERT component is responsible for AI-based vulnerability prediction.

The general workflow is:

```text
Java Source Code
       |
       v
Tokenizer
       |
       v
CodeBERT
       |
       v
Model Output
       |
       v
Prediction Label
       |
       v
Confidence Score
```

---

# Confidence Score

The confidence score represents the model's prediction confidence according to the current model implementation.

Example:

```text
CWE-78
33.37%
```

The frontend converts the confidence value into a percentage display.

For example:

```text
33.37%
```

The progress bar is also updated according to the confidence.

---

# Static Analysis

Static analysis runs independently from the CodeBERT prediction.

The static-analysis component looks for patterns in the Java source code.

For example:

```java
String input = null;

System.out.println(input.length());
```

This may produce an issue such as:

```text
Null Safety

Object method is called without an obvious null check.

Severity: MEDIUM
```

Another example:

```java
System.out.println("Hello");
```

may produce:

```text
Code Quality

System.out.println found. Consider using a logging framework.

Severity: LOW
```

---

# Testing the Application

After starting both services:

1. Open the frontend.
2. Verify that the API status says:

```text
API Online
```

3. Paste Java source code.
4. Click:

```text
Analyze Code
```

5. Wait for the backend response.
6. Check the AI Prediction section.
7. Check the Static Analysis section.

---

# Example Java Code

## Example 1 - Simple Java Program

```java
public class Test {

    public static void main(String[] args) {

        int a = 10;
        int b = 20;

        int sum = a + b;

        System.out.println("Sum = " + sum);
    }
}
```

This can be used to test basic communication between the frontend and backend.

---

# Example 2 - Null Safety Test

```java
public class Test {

    public static void main(String[] args) {

        String input = null;

        System.out.println(input.length());
    }
}
```

This is useful for testing static analysis related to null safety.

---

# Example 3 - SQL Injection Test

```java
import java.sql.*;

public class Test {

    public static void main(String[] args) throws Exception {

        String user = "admin";

        Connection con = DriverManager.getConnection(
            "jdbc:mysql://localhost/test",
            "root",
            "password"
        );

        Statement stmt = con.createStatement();

        String query =
            "SELECT * FROM users WHERE name = '" + user + "'";

        ResultSet rs = stmt.executeQuery(query);

        System.out.println(rs);
    }
}
```

This is useful for testing security-related static analysis and AI prediction.

---

# Expected Results

After submitting code, the application should display something similar to:

```text
AI Prediction

Predicted Vulnerability
CWE-78

Confidence
33.37%
```

And below it:

```text
Static Analysis

2 Issues
```

For example:

```text
Null Safety
MEDIUM

Object method is called without an obvious null check.
```

and:

```text
Code Quality
LOW

System.out.println found.
Consider using a logging framework.
```

The actual results depend on the backend implementation and model prediction.

---

# Testing Different Java Programs

To properly test the system, use different categories of Java programs.

## Test 1 - Clean Code

```java
public class Calculator {

    public static int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        int result = add(10, 20);
    }
}
```

---

## Test 2 - Null Safety

```java
public class Test {

    public static void main(String[] args) {

        String value = null;

        System.out.println(value.length());
    }
}
```

---

## Test 3 - SQL Injection

```java
String query =
    "SELECT * FROM users WHERE name = '" + user + "'";
```

---

## Test 4 - System Output

```java
public class Test {

    public static void main(String[] args) {

        System.out.println("Debug message");
    }
}
```

---

## Test 5 - Multiple Issues

```java
public class Test {

    public static void main(String[] args) {

        String input = null;

        System.out.println(input.length());

        System.out.println("Debug");

    }
}
```

This is useful for checking whether multiple static-analysis issues are displayed correctly.

---

# Troubleshooting

## Problem: API Offline

If the frontend displays:

```text
API Offline
```

check that the backend is running.

Start the backend:

```bash
uvicorn backend.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/health
```

---

# Problem: Failed to Fetch

If the browser console shows:

```text
Failed to fetch
```

check:

1. Backend is running.
2. Backend URL is correct.
3. `/analyze` endpoint exists.
4. CORS is configured.
5. Port number is correct.

The frontend should use:

```text
http://127.0.0.1:8000/analyze
```

---

# Problem: HTTP 404

If the console shows:

```text
HTTP Status: 404
```

the requested endpoint does not exist.

Check:

```text
/analyze
```

in `backend/app.py`.

---

# Problem: HTTP 422

If the backend returns:

```text
422 Unprocessable Entity
```

the request body probably does not match the FastAPI request model.

Check the frontend JSON.

For example:

```javascript
body: JSON.stringify({
    code: code
})
```

must match the backend model.

---

# Problem: HTTP 500

If the backend returns:

```text
500 Internal Server Error
```

check the backend terminal.

There may be an exception in:

* Static analysis.
* Tokenization.
* CodeBERT.
* Model loading.
* Request processing.

---

# Problem: Prediction Does Not Change

If different Java programs always produce exactly the same prediction, check:

1. Whether the frontend is sending the new code.
2. Whether `/analyze` receives the new code.
3. Whether the backend actually passes the received code to CodeBERT.
4. Whether the model is loaded correctly.
5. Whether the prediction logic is hardcoded.

The browser console should show the submitted Java code.

---

# Problem: Static Analysis Does Not Change

If static-analysis results remain the same for every program, check the static-analysis function.

The function should receive the Java source code submitted by the user.

The backend should perform analysis on the current request rather than returning hardcoded results.

---

# Problem: Frontend Shows Old Results

If the UI continues showing previous results:

1. Refresh the page.
2. Clear the browser cache if necessary.
3. Check the JavaScript console.
4. Confirm the latest backend response.
5. Make sure the results section is updated after every request.

---

# Browser Console Debugging

Open browser developer tools:

```text
F12
```

Then select:

```text
Console
```

Useful debugging messages include:

```text
Backend is online.
```

```text
Sending Java code to backend...
```

```text
URL: http://127.0.0.1:8000/analyze
```

```text
HTTP Status: 200
```

```text
BACKEND RESPONSE:
```

```text
Displaying backend data:
```

These messages help verify the complete frontend-backend communication.

---

# Development Workflow

When modifying the backend:

1. Save `app.py`.
2. Uvicorn reloads the backend automatically if `--reload` is enabled.
3. Test `/health`.
4. Test `/analyze`.
5. Refresh the frontend.
6. Submit Java code again.

When modifying the frontend:

1. Save the HTML/CSS/JavaScript file.
2. Live Server automatically reloads the page.
3. Open browser developer tools.
4. Submit Java code.
5. Verify the response.

---

# Recommended Development Setup

Use two terminals.

## Terminal 1

```bash
uvicorn backend.app:app --reload
```

## Terminal 2

Run the frontend using VS Code Live Server.

This makes it easy to modify both frontend and backend independently.

---

# API Testing Without Frontend

The backend can also be tested directly through FastAPI Swagger.

Open:

```text
http://127.0.0.1:8000/docs
```

Find:

```text
POST /analyze
```

Click:

```text
Try it out
```

Enter Java source code.

Then click:

```text
Execute
```

The API response should be displayed directly.

This is useful when debugging whether the problem is in the backend or frontend.

---

# Frontend vs Backend Debugging

If the backend Swagger returns the correct response but the frontend does not display it, the problem is most likely in:

```text
frontend/script.js
```

If Swagger itself returns an incorrect response, the problem is most likely in:

```text
backend/app.py
```

or the model/static-analysis implementation.

---

# Recommended Debugging Flow

Use this order:

```text
1. Check backend startup
        |
        v
2. Open /health
        |
        v
3. Open /docs
        |
        v
4. Test POST /analyze
        |
        v
5. Check backend JSON
        |
        v
6. Open frontend
        |
        v
7. Check API Online
        |
        v
8. Submit Java code
        |
        v
9. Check browser console
        |
        v
10. Check UI result
```

---

# Security Considerations

This project is intended primarily for development and research purposes.

Java source code submitted to the backend should be treated as untrusted input.

The backend should not compile or execute arbitrary Java code unless a secure sandboxing mechanism is implemented.

Important security considerations include:

* Validate input size.
* Restrict request sizes.
* Do not execute submitted source code directly.
* Avoid exposing sensitive model files.
* Use HTTPS in production.
* Restrict CORS origins in production.
* Validate API requests.
* Protect backend endpoints.
* Avoid logging sensitive source code in production.
* Use authentication if the system is deployed publicly.

---

# Important: Source Code Is Analyzed, Not Executed

The intended workflow is:

```text
Java Source Code
       |
       v
Static Analysis
       |
       v
CodeBERT
       |
       v
Prediction
```

The submitted Java program should not need to be executed to perform the analysis.

This is important because executing arbitrary source code submitted by users can create serious security risks.

---

# Limitations

The current system has several limitations.

## 1. Model Accuracy

The CodeBERT model's prediction quality depends on:

* Training dataset.
* Dataset quality.
* Training process.
* Class distribution.
* Model architecture.
* Fine-tuning process.

The confidence score should not automatically be treated as a guaranteed probability of vulnerability.

---

## 2. Static Analysis Coverage

Static analysis can only detect patterns that have been implemented.

It cannot automatically detect every possible Java vulnerability.

---

## 3. False Positives

The system may report an issue even when the code is actually safe.

---

## 4. False Negatives

The system may fail to detect an actual vulnerability.

---

## 5. CWE Prediction

The predicted CWE should be treated as an AI-assisted prediction rather than a definitive security classification.

---

# Future Improvements

The project can be extended with additional features.

## 1. More CWE Classes

Support more vulnerability categories such as:

```text
CWE-22
CWE-78
CWE-79
CWE-89
CWE-119
CWE-125
CWE-190
CWE-287
CWE-416
CWE-476
```

The exact classes depend on the training dataset.

---

## 2. Better Static Analysis

Add additional rules for:

* SQL Injection.
* Command Injection.
* Path Traversal.
* Hardcoded credentials.
* Weak cryptography.
* Unsafe deserialization.
* Insecure randomness.
* Authentication problems.
* Authorization problems.
* Resource leaks.

---

## 3. Line Numbers

Static-analysis results can be improved by reporting the exact source-code line.

Example:

```text
Line 12

Null Safety
Object method is called without an obvious null check.
```

---

## 4. Code Highlighting

The frontend could highlight vulnerable code directly inside the editor.

---

## 5. Detailed Recommendations

Instead of only reporting:

```text
SQL Injection
```

the system could provide:

```text
Recommendation:

Use PreparedStatement instead of constructing SQL queries
using string concatenation.
```

---

## 6. Downloadable Reports

The application could allow users to download:

```text
PDF
JSON
CSV
HTML
```

reports.

---

## 7. GitHub Integration

The system could analyze Java files directly from GitHub repositories.

---

## 8. CI/CD Integration

The analyzer could be integrated into:

```text
GitHub Actions
GitLab CI
Jenkins
AWS CodePipeline
```

and automatically analyze code during development.

---

## 9. Cloud Deployment

The application can be deployed using cloud infrastructure such as:

```text
AWS
Azure
Google Cloud
Vercel
```

The architecture can be modified so that the frontend and backend are deployed independently.

---

# Project Goals

The main goals of the project are:

1. Build a practical Java source-code analysis system.
2. Combine traditional static analysis with machine learning.
3. Use CodeBERT for vulnerability prediction.
4. Provide an easy-to-use web interface.
5. Establish frontend-backend communication through REST APIs.
6. Display real-time analysis results.
7. Provide a foundation for future security-analysis improvements.

---

# Example Complete Workflow

A user enters:

```java
public class Test {

    public static void main(String[] args) {

        String input = null;

        System.out.println(input.length());

    }
}
```

The frontend sends:

```http
POST /analyze
```

with:

```json
{
    "code": "public class Test {...}"
}
```

The backend performs:

```text
Static Analysis
       +
CodeBERT Prediction
```

The backend returns:

```json
{
    "success": true,
    "prediction": {
        "label": "CWE-78",
        "confidence": 32.26
    },
    "static_analysis": [
        {
            "type": "Null Safety",
            "message": "Object method is called without an obvious null check.",
            "severity": "MEDIUM"
        },
        {
            "type": "Code Quality",
            "message": "System.out.println found. Consider using a logging framework.",
            "severity": "LOW"
        }
    ]
}
```

The JavaScript frontend receives the response and updates the page:

```text
AI Prediction

CWE-78

Confidence

32.26%
```

and:

```text
Static Analysis

2 Issues

Null Safety
MEDIUM

Object method is called without an obvious null check.

Code Quality
LOW

System.out.println found.
Consider using a logging framework.
```

---

# Testing Checklist

Before considering the application working correctly, verify all of the following:

* [ ] Backend starts successfully.
* [ ] CodeBERT model loads successfully.
* [ ] `/health` returns successfully.
* [ ] `/docs` opens successfully.
* [ ] `/analyze` accepts Java code.
* [ ] Backend returns HTTP 200 for valid requests.
* [ ] Backend returns valid JSON.
* [ ] Frontend starts using Live Server.
* [ ] Frontend displays API Online.
* [ ] Java code can be entered.
* [ ] Analyze Code button works.
* [ ] Frontend sends the submitted code.
* [ ] Backend receives the submitted code.
* [ ] AI prediction is returned.
* [ ] Confidence is returned.
* [ ] Static-analysis results are returned.
* [ ] Issue count is updated.
* [ ] Issues are dynamically displayed.
* [ ] Severity is displayed.
* [ ] Different Java programs can be tested.
* [ ] Errors are displayed properly.

---

# Conclusion

The Java Defect Prediction System combines machine learning and static analysis into a single web-based Java security-analysis application.

The system provides:

```text
Java Source Code
        |
        v
      FastAPI
        |
        +----------------+
        |                |
        v                v
Static Analysis      CodeBERT
        |                |
        +-------+--------+
                |
                v
          JSON Response
                |
                v
           JavaScript
                |
                v
         Web Interface
```

This architecture provides a foundation for building a more advanced automated Java vulnerability-detection platform.

The project can be further improved by expanding the static-analysis rules, improving the machine-learning model, supporting more CWE categories, adding line-level vulnerability detection, generating reports, and integrating the system into CI/CD pipelines.

---

# Author

**Java Defect Prediction System**

A software engineering and machine-learning project focused on Java source-code security analysis using:

* Static Analysis
* CodeBERT
* FastAPI
* JavaScript
* HTML
* CSS

---

```
```
