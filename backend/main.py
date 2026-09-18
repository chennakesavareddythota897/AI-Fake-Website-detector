from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import joblib
import os
from datetime import datetime

from features import extract_features, features_to_vector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "scans.db"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

model = joblib.load(MODEL_PATH)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            reasons TEXT NOT NULL,
            scanned_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


def build_reasons(feat: dict) -> list:
    reasons = []
    reasons.append("HTTPS Enabled" if feat["is_https"] else "No HTTPS")

    if feat["is_trusted"]:
        reasons.append("Trusted Domain")
    else:
        reasons.append("Domain Not in Trusted List")

    if feat["is_ip_domain"]:
        reasons.append("Uses IP Address Instead of Domain")

    if feat["keyword_count"] > 0:
        reasons.append(f"{feat['keyword_count']} Suspicious Keyword(s) Found")

    if feat["hyphen_count"] >= 2:
        reasons.append("Multiple Hyphens in Domain")

    if feat["subdomain_count"] > 3:
        reasons.append("Too Many Subdomains")

    if feat["url_length"] > 75:
        reasons.append("Unusually Long URL")

    if feat["at_symbol"]:
        reasons.append("Contains '@' Symbol (Common Phishing Trick)")

    return reasons


@app.get("/")
def home():
    return {"message": "Backend Running Successfully"}


@app.get("/scan")
def scan(url: str = Query(..., description="Website URL to scan")):
    feat = extract_features(url)
    vector = [features_to_vector(feat)]

    phishing_probability = model.predict_proba(vector)[0][1]
    risk = int(round(phishing_probability * 100))

    status = "🔴 PHISHING" if risk > 70 else ("🟠 SUSPICIOUS" if risk > 30 else "🟢 SAFE")
    reasons = build_reasons(feat)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scans (url, status, risk_score, reasons, scanned_at) VALUES (?, ?, ?, ?, ?)",
        (url, status, risk, ", ".join(reasons), datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()

    return {
        "url": url,
        "status": status,
        "riskScore": risk,
        "reasons": reasons,
        "details": feat,
    }


@app.get("/history")
def history(limit: int = 20):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, url, status, risk_score, reasons, scanned_at FROM scans ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "url": row["url"],
            "status": row["status"],
            "riskScore": row["risk_score"],
            "reasons": row["reasons"].split(", "),
            "scannedAt": row["scanned_at"],
        }
        for row in rows
    ]