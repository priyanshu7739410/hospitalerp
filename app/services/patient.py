from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

class PatientService:
    @staticmethod
    def get_patient(db: Session, patient_id: int):
        # db.query(Patient).filter(...).first() translates exactly to:
        # SELECT * FROM patients WHERE id = patient_id LIMIT 1;
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with ID {patient_id} not found."
            )
        return patient

    @staticmethod
    def get_patient_by_email(db: Session, email: str):
        return db.query(Patient).filter(Patient.email == email).first()

    @staticmethod
    def get_patients(db: Session, skip: int = 0, limit: int = 100):
        # offset(skip).limit(limit) is standard pagination.
        # It prevents loading 100,000 patients into RAM at once.
        return db.query(Patient).offset(skip).limit(limit).all()

    @staticmethod
    def create_patient(db: Session, patient: PatientCreate):
        # Check if email already exists
        existing_patient = PatientService.get_patient_by_email(db, email=patient.email)
        if existing_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )
        
        # Convert Pydantic schema dictionary to SQLAlchemy model instance
        db_patient = Patient(**patient.model_dump())
        
        # Step 1: Add to current session
        db.add(db_patient)
        # Step 2: Commit (physically save to PostgreSQL)
        db.commit()
        # Step 3: Refresh (fetch the newly generated ID and created_at from Postgres)
        db.refresh(db_patient)
        
        return db_patient

    @staticmethod
    def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate):
        db_patient = PatientService.get_patient(db, patient_id)
        
        # model_dump(exclude_unset=True) is a crucial Pydantic feature.
        # It returns ONLY the fields the user explicitly sent in their request.
        # If they only sent 'phone', it ignores first_name, email, etc.
        update_data = patient_update.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_patient, key, value)
            
        db.commit()
        db.refresh(db_patient)
        return db_patient
