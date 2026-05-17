from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.patient import PatientService

# Step 1: Initialize APIRouter
# Notice prefix="/api/v1/patients". Every route below will automatically start with this URL.
# tags=["Patients"] groups these endpoints beautifully inside the FastAPI Swagger UI.
router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])

# Step 2: Create Patient Endpoint
# response_model=PatientResponse: Tells FastAPI to take whatever PatientService returns, pass it through PatientResponse schema, and convert to clean JSON.
@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Notice how thin the router is! Just one line calling the service.
    return PatientService.create_patient(db, patient)

# Step 3: Get All Patients Endpoint
@router.get("/", response_model=List[PatientResponse])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return PatientService.get_patients(db, skip=skip, limit=limit)

# Step 4: Get Single Patient Endpoint
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return PatientService.get_patient(db, patient_id)

# Step 5: Update Patient Endpoint
@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    return PatientService.update_patient(db, patient_id, patient_update)
