from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Float, text, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base 

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # Added role for RBAC logic
    role = Column(String(20), server_default=text("'viewer'")) 
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    
    datasets = relationship("Dataset", back_populates="owner")

class Dataset(Base):
    __tablename__ = "datasets"
    dataset_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    size_mb = Column(Float)
    status = Column(String(20), server_default=text("'uploaded'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(Boolean, default=False, nullable=False) 
    
    owner = relationship("User", back_populates="datasets")

class TrainingJob(Base):
    __tablename__ = "training_jobs"
    job_id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.dataset_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), server_default=text("'pending'"))
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    dataset = relationship("Dataset")
    user = relationship("User")

class TrainedModel(Base):
    __tablename__ = "models"
    model_id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("training_jobs.job_id", ondelete="CASCADE"), nullable=False)
    version = Column(String(20), nullable=False)
    accuracy = Column(Float, default=0.0)
    file_path = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    job = relationship("TrainingJob")