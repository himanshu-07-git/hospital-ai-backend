#  Hospital AI Backend

A simple FastAPI backend that simulates a hospital receptionist system.  

It handles patient conversations step by step, collects basic details, and classifies them into appropriate wards.
---
## Features
- Handles patient conversations in sessions
- Collects patient details: name, age, symptoms
- Classifies patients into wards:
  - Emergency
  - Mental Health
  - General
- Sends data to a webhook (example with HTTPX)
---
## Tech Stack
- Python 3.12+
- FastAPI
- Uvicorn
- HTTPX
---
## How to Run Locally

1. Open terminal in `backend` folder
2. Install dependencies:

```bash
pip install -r requirements.txt
