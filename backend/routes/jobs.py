import asyncio
import random
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import sqlalchemy_models as models, pydantic_schemas as schemas
from ..core import database, limiter, auth # Added auth for token dependency

router = APIRouter(tags=["Training Jobs"])

@router.post("/create", response_model=schemas.TrainingJobOut)
def create_training_job(
    job: schemas.TrainingJobCreate, 
    db: Session = Depends(database.get_db),
    token: str = Depends(auth.oauth2_scheme) # Forces login to start a job
):
    # 1. Apply Rate Limiting (60-second cooldown)
    can_proceed, wait_time = limiter.check_rate_limit(job.user_id, seconds=60)
    if not can_proceed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Please wait {wait_time}s before starting another job."
        )

    # 2. Verify Dataset exists
    db_dataset = db.query(models.Dataset).filter(
        models.Dataset.dataset_id == job.dataset_id,
        models.Dataset.is_deleted == False # Safety check for soft deletes
    ).first()
    
    if not db_dataset:
        raise HTTPException(status_code=404, detail="Dataset not found or has been deleted")
    
    # 3. Create Job
    new_job = models.TrainingJob(
        dataset_id=job.dataset_id,
        user_id=job.user_id,
        status="pending"
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.post("/simulate/{job_id}")
async def simulate_training(job_id: int, db: Session = Depends(database.get_db)):
    job = db.query(models.TrainingJob).filter(models.TrainingJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = "running"
    job.start_time = datetime.now(timezone.utc)
    db.commit()

    final_loss, final_acc = 0.0, 0.0

    for epoch in range(1, 6):
        final_loss = round(random.uniform(0.1, 0.5), 4)
        final_acc = round(random.uniform(0.7, 0.99), 4)

        log_entry = {
            "job_id": job_id,
            "epoch": epoch,
            "loss": final_loss,
            "accuracy": final_acc,
            "timestamp": datetime.now(timezone.utc)
        }
        # Logging to MongoDB (NoSQL)
        await database.experiment_collection.insert_one(log_entry)
        await asyncio.sleep(1) # Simulate time-consuming AI compute

    job.status = "completed"
    job.end_time = datetime.now(timezone.utc)
    db.commit()
    db.refresh(job)

    return {"status": "Success", "final_metrics": {"loss": final_loss, "accuracy": final_acc}}

@router.post("/register-model", response_model=schemas.ModelOut)
def register_trained_model(model_data: schemas.ModelRegister, db: Session = Depends(database.get_db)):
    job = db.query(models.TrainingJob).filter(models.TrainingJob.job_id == model_data.job_id).first()
    
    if not job or job.status != "completed":
        raise HTTPException(status_code=400, detail="Job must be completed before registering a model")

    new_model = models.TrainedModel(
        job_id=model_data.job_id,
        version=model_data.version,
        accuracy=model_data.accuracy,
        file_path=model_data.file_path
    )
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

@router.get("/{job_id}/logs", response_model=List[schemas.EpochLogOut])
async def get_training_logs(job_id: int):
    # Fetching from MongoDB
    cursor = database.experiment_collection.find({"job_id": job_id}).sort("epoch", 1)
    logs = await cursor.to_list(length=100)
    if not logs:
        raise HTTPException(status_code=404, detail="No training logs found for this job")
    return logs

@router.get("/models/all", response_model=List[schemas.ModelOut])
def get_all_models(db: Session = Depends(database.get_db)):
    return db.query(models.TrainedModel).all()