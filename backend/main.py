from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import randint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":"Backend Running Successfully"}

@app.get("/scan")
def scan():
   risk = randint(0, 100)

   if risk > 70:
       return {
           "status": "🔴 PHISHING",
           "riskScore": risk,
           "reasons": [
               "No HTTPS",
               "Blacklisted Website"

           ]
             }
   else:
       return {
           "status": "🟢 SAFE",
           "riskScore": risk,
           "reasons": [
               "HTTPS Enabled",
               "Trusted Domain"
           ]
       }