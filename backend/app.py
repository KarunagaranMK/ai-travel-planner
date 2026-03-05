from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import TravelRequest
from rag_travel_agent import plan_trip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "AI Travel Planner Backend Running 🚀"}


@app.post("/plan-trip")
def create_trip(request: TravelRequest):
    result, reasoning = plan_trip(
        request.destination,
        request.days,
        request.budget
    )

    if not result:
        return {"error": reasoning}

    return {
        "user": request.name,
        "trip_plan": result,
        "reasoning": reasoning
    }