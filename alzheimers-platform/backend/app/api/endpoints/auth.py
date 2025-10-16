# backend/app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ... import schemas, services, models
from ...database import get_db

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = services.auth.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    # Check MFA if enabled for user
    if user.mfa_secret:
        # Implement MFA verification logic
        pass

    access_token = services.auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# backend/app/api/endpoints/intakes.py
@router.post("/intakes", response_model=schemas.Intake)
def create_intake(
    intake: schemas.IntakeCreate,
    current_user: models.User = Depends(services.auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify user has permission to create intake
    if current_user.role not in ["patient", "nurse", "doctor"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )

    return services.intakes.create_intake(db=db, intake=intake, user_id=current_user.id)