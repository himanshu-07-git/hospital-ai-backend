from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#  CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Patient(BaseModel):
    message: str
    session_id: str

user_sessions = {}

def classify_ward(query):
    query = query.lower()
    if "pain" in query or "accident" in query or "bleeding" in query:
        return "Emergency"
    elif "stress" in query or "depression" in query:
        return "Mental Health"
    else:
        return "General"

#  Home route
@app.get("/")
def home():
    return {"message": "Hospital AI Backend Running 🚀"}

#  Chat route
@app.post("/chat")
async def chat(data: Patient):
    session_id = data.session_id
    msg = data.message.strip()

    if not msg:
        return {"reply": " Please enter a valid message"}

    # create session
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "name": None,
            "age": None,
            "query": None,
            "ward": None
        }

    user_data = user_sessions[session_id]

    try:
        # Step 1: Query
        if user_data["query"] is None:
            user_data["query"] = msg
            user_data["ward"] = classify_ward(msg)
            return {"reply": "Please tell your name"}

        # Step 2: Name
        if user_data["name"] is None:
            user_data["name"] = msg
            return {"reply": "Please tell your age"}

        # Step 3: Age
        if user_data["age"] is None:
            if not msg.isdigit():
                return {"reply": " Please enter a valid age (number)"}

            user_data["age"] = msg

            payload = {
                "patient_name": user_data["name"],
                "patient_age": user_data["age"],
                "patient_query": user_data["query"],
                "ward": user_data["ward"],
                "timestamp": str(datetime.now())
            }

            #  FIXED PART
            try:
                async with httpx.AsyncClient() as client:
                    await client.post("https://httpbin.org/post", json=payload)
            except:
                print("Webhook failed")

            response = f" Registered!\nWard: {user_data['ward']}"

            user_sessions.pop(session_id, None)

            return {"reply": response}

    except Exception as e:
        print("ERROR:", e)
        return {"reply": " Server crashed, check backend"}
