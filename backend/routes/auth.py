from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import sqlalchemy_models as models, pydantic_schemas as schemas
from ..core.database import get_db
from ..core import auth  # Import our new utility
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# --- REGISTER ---
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash the password before saving!
    hashed_pwd = auth.get_password_hash(user.password)
    
    # 3. Create new user with role support
    new_user = models.User(
        name=user.name, 
        email=user.email, 
        password_hash=hashed_pwd,
        role=user.role  # Taken from UserCreate schema
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), # Use this instead of schemas.UserCreate
    db: Session = Depends(get_db)
):
    # 1. Fetch User (Note: OAuth2 uses 'username' field even for emails)
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Verify password
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate Token
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_name": user.name
    }