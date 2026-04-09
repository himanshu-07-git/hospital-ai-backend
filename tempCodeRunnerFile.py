from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import requests

app = FastAPI()

class Patient(BaseModel):
    message: str

# temporary memory (for demo)
user_data = {
    "name": None,
    "age": None,
    "query": None,
    "ward": None
}

def classify_ward(query):
    query = query.lower()
    if "pain" in query or "accident" in query or "bleeding" in query:
        return "Emergency"
    elif "stress" in query or "depression" in query:
        return "Mental Health"
    else:
        return "General"

@app.post("/chat")
def chat(data: Patient):
    msg = data.message

    # Step 1: Get query
    if user_data["query"] is None:
        user_data["query"] = msg
        user_data["ward"] = classify_ward(msg)
        return {"reply": "Please tell your name"}

    # Step 2: Get name
    elif user_data["name"] is None:
        user_data["name"] = msg
        return {"reply": "Please tell your age"}

    # Step 3: Get age
    elif user_data["age"] is None:
        user_data["age"] = msg

        payload = {
            "patient_name": user_data["name"],
            "patient_age": user_data["age"],
            "patient_query": user_data["query"],
            "ward": user_data["ward"],
            "timestamp": str(datetime.now())
        }

        #  Webhook (optional, won’t crash if fails)
        try:
            requests.post("https://httpbin.org/post", json=payload)
        except:
            pass

        response = f" Registered!\nWard: {user_data['ward']}"

        # reset for next user
        for key in user_data:
            user_data[key] = None

        return {"reply": response}
