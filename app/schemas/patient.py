from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date, datetime
from typing import Optional

# Step 1: Base Schema
# This contains attributes common across all patient requests and responses.
# By putting them in a Base class, we don't have to retype them 10 times.
class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, description="Patient's first name")
    last_name: str = Field(..., min_length=2, max_length=50, description="Patient's last name")
    # EmailStr automatically validates that the string looks like a real email (user@domain.com)
    email: EmailStr = Field(..., description="Unique email address")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone number")
    date_of_birth: date = Field(..., description="Date of birth in YYYY-MM-DD format")
    gender: str = Field(..., description="Gender (e.g., Male, Female, Other)")
    blood_group: Optional[str] = Field(None, max_length=5, description="Blood group (e.g., A+, O-)")
    is_active: bool = True

# Step 2: Create Schema
# Used specifically when a user sends a POST request to register a new patient.
# It inherits everything from PatientBase. Notice it does NOT have an 'id' field, because the DB creates the ID.
class PatientCreate(PatientBase):
    pass

# Step 3: Update Schema
# Used when updating a patient. All fields are optional because the user might only want to update their phone number.
class PatientUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    is_active: Optional[bool] = None

# Step 4: Response Schema
# This is what we return back to the frontend/user after fetching from the DB.
class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # model_config = ConfigDict(from_attributes=True) is a CRITICAL PYDANTIC FEATURE.
    # In Python, SQLAlchemy returns objects (patient.first_name). Pydantic normally expects dictionaries (patient['first_name']).
    # Setting from_attributes=True tells Pydantic: "If you receive a SQLAlchemy object, automatically read its attributes and convert to JSON."
    model_config = ConfigDict(from_attributes=True)
