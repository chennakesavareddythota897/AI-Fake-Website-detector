# AI-Powered Browser Extension for Fake Website Detection

A Chrome browser extension (Manifest V3) that analyzes websites in real time and detects phishing/fake websites using a trained Machine Learning model, backed by a FastAPI service.

## Features

- Real-time website scanning - scans the currently active tab's URL automatically
- AI-powered phishing detection - trained scikit-learn (Random Forest) classifier
- Security risk scoring - 0-100% phishing probability score
- Browser warning popup - prominent warning banner for high-risk sites
- Threat analysis report - detailed feature-level breakdown per scan
- Scan history dashboard - past scans stored and viewable
- REST API backend - FastAPI service with auto-generated docs

## Tech Stack

| Layer | Technology |
|---|---|
| Extension | JavaScript, HTML/CSS, React (Vite), Chrome Extension Manifest V3 |
| Backend | Python, FastAPI |
| ML | scikit-learn (RandomForestClassifier) |
| Database | SQLite |
| API Docs | FastAPI auto-generated Swagger / ReDoc |

## Project Structure

    AI-Fake-Website-Detector/
    |-- backend/
    |   |-- main.py              (FastAPI app: /scan, /history endpoints)
    |   |-- features.py          (Shared URL feature-extraction logic)
    |   |-- generate_dataset.py  (Generates the training dataset)
    |   |-- train_model.py       (Trains and saves the ML model)
    |   |-- model.pkl            (Trained model, generated)
    |   `-- scans.db             (SQLite scan history, generated)
    |-- frontend/frontend/       (React + Vite app - popup UI)
    |   |-- src/
    |   |   |-- App.jsx
    |   |   `-- components/
    |   `-- dist/                (Production build used by the extension)
    |-- manifest.json            (Chrome extension manifest V3)
    |-- background.js            (Extension service worker)
    `-- README.md

## How It Works

1. The extension popup reads the active browser tab's URL (chrome.tabs.query).
2. On "Scan Website", the URL is sent to the FastAPI backend (GET /scan?url=...).
3. The backend extracts 9 numeric features from the URL (HTTPS usage, trusted-domain match, IP-based domain, URL length, suspicious keyword count, subdomain count, hyphen count, digit ratio, @ symbol presence).
4. These features are passed to a trained RandomForestClassifier, which outputs a phishing probability.
5. The result (status, risk score, reasons, and full feature breakdown) is returned to the extension and logged to SQLite.
6. If the risk score is high, a warning banner is shown in the popup.

## Setup and Running Locally

### 1. Backend (FastAPI + ML)

    cd backend
    python -m venv venv
    venv\Scripts\activate        (Windows)
    pip install fastapi uvicorn scikit-learn pandas joblib numpy
    python generate_dataset.py
    python train_model.py
    uvicorn main:app --reload --port 8000

Backend runs at http://127.0.0.1:8000. Interactive API docs are available at http://127.0.0.1:8000/docs

### 2. Frontend (React + Vite)

    cd frontend/frontend
    npm install
    npm run dev
    npm run build

### 3. Load the Chrome Extension

1. Run npm run build inside frontend/frontend (this creates dist/).
2. Open chrome://extensions in Chrome.
3. Enable Developer mode (top-right toggle).
4. Click Load unpacked and select the project's root folder (AI-Fake-Website-Detector).
5. Pin the extension and click its icon on any website to scan it.

Note: The FastAPI backend must be running on 127.0.0.1:8000 for the extension to work.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| GET | /scan?url=<url> | Scans a URL and returns risk score, status, reasons, and feature details |
| GET | /history?limit=<n> | Returns the most recent scans (default 20) |

Full interactive documentation: http://127.0.0.1:8000/docs

## Model Details

- Algorithm: RandomForestClassifier (scikit-learn), 200 trees, max depth 8
- Training data: Synthetically generated dataset (3,000 URLs) modeled on real-world phishing patterns (IP-based URLs, keyword stuffing, typosquatting, suspicious TLDs) and a curated list of legitimate domains
- Features used: HTTPS usage, trusted-domain match, IP-based domain, URL length, suspicious keyword count, subdomain count, hyphen count, digit ratio in domain, presence of @ symbol
- Retraining: Run "python generate_dataset.py" then "python train_model.py" inside backend/ to regenerate model.pkl

## Known Limitations

- The training dataset is synthetically generated rather than sourced from a live phishing feed (e.g. PhishTank/OpenPhish); real-world accuracy may vary.
- The trusted-domain list is a fixed allowlist and should be expanded for broader coverage.
- No user authentication - scan history is local to the machine running the backend.

## Author

Chennakesavareddy - Internship Project, AI-Powered Browser Extension for Fake Website Detection