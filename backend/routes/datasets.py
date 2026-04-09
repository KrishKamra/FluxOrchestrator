import shutil
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..models import sqlalchemy_models as models, pydantic_schemas as schemas
from ..core.database import get_db
from jose import jwt
from ..core.auth import SECRET_KEY, ALGORITHM # Import your security constants

# Import the scheme from your main or auth core to resolve the squiggly error
from ..core.auth import oauth2_scheme 

router = APIRouter(tags=["Datasets"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/{user_id}")
async def upload_dataset(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = UPLOAD_DIR / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    new_dataset = models.Dataset(
        name=file.filename,
        file_path=str(file_path),
        owner_id=user_id,
        size_mb=file_path.stat().st_size / (1024 * 1024),
        is_deleted=False 
    )
    
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    
    return {"message": "Dataset uploaded successfully", "dataset_id": new_dataset.dataset_id}

@router.get("/{user_id}", response_model=List[schemas.DatasetOut])
def get_user_datasets(user_id: int, db: Session = Depends(get_db)):
    """Fetches only datasets that have NOT been soft-deleted."""
    datasets = db.query(models.Dataset).filter(
        models.Dataset.owner_id == user_id, 
        models.Dataset.is_deleted == False
    ).all()
    return datasets if datasets else []

@router.delete("/delete/{dataset_id}")
def soft_delete_dataset(
    dataset_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # 1. Decode the token to verify identity and role
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_role = payload.get("role")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 2. RBAC Logic: Only 'admin' can perform soft deletes
    if user_role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: Only Admins can delete datasets"
        )

    # 3. Proceed with soft delete if role is Admin
    dataset = db.query(models.Dataset).filter(models.Dataset.dataset_id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    dataset.is_deleted = True 
    db.commit()
    return {"message": f"Dataset {dataset_id} moved to trash by Admin"}