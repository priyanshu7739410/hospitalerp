from fastapi import FastAPI

# Step 1: Initialize the FastAPI application
# This 'app' variable is exactly what Uvicorn looks for when we run:
# uvicorn app.main:app
from app.routers import patient

app = FastAPI(
    title="Hospital ERP API",
    description="Backend API for Hospital Management System",
    version="1.0.0"
)

# Include the patient module router
app.include_router(patient.router)

# Step 2: Define a simple root endpoint
# The @app.get("/") is a decorator. It tells FastAPI:
# "Whenever a user makes a GET request to the root URL (http://localhost:8000/), run this function."
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Hospital ERP System!",
        "status": "Server is running perfectly inside Docker."
    }
