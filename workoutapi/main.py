from fastapi import FastAPI

from workoutapi.routes import api_router

app = FastAPI(title="WorkoutAPI")
app.include_router(api_router)
