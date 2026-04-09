from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- AUTH SCHEMAS ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str
    email: str
    role: str = "viewer"

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- DATASET SCHEMAS ---
class DatasetOut(BaseModel):
    dataset_id: int
    name: str
    file_path: str
    size_mb: Optional[float] = 0.0
    status: Optional[str] = "uploaded"
    created_at: Optional[datetime] = None
    is_deleted: bool

    class Config:
        from_attributes = True

# --- JOB & MODEL SCHEMAS ---
class TrainingJobCreate(BaseModel):
    dataset_id: int
    user_id: int

class TrainingJobOut(BaseModel):
    job_id: int
    dataset_id: int
    user_id: int
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class ModelRegister(BaseModel):
    job_id: int
    version: str
    accuracy: float
    file_path: str

class ModelOut(BaseModel):
    model_id: int
    job_id: int
    version: str
    accuracy: float
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True

class EpochLogOut(BaseModel):
    epoch: int
    loss: float
    accuracy: float
    timestamp: datetime

    class Config:
        from_attributes = True