from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    UserCreate,
    UserLogin,
    EmailRequest,
    PasswordResetRequest,
    TokenRefreshRequest,
    UserOut,
    toggleStatus,
    UserUpdate,
)
from .auth_utils import (
    create_access_token,
    verify_password,
    hashed_password,
    create_refresh_token,
    decode_refresh_token,
    get_current_user,
)
from fastapi.responses import JSONResponse
from app.models import User, RoleEnum, Status

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(email=user.email).first()
        if existing_user:
            return JSONResponse(status_code=400, content={"success": False, "message": "Email already registered"})
        if user.role not in [role.value for role in RoleEnum]:
            return JSONResponse(status_code=400,content={"success": False, "message": "Invalid role"})

        new_user = User(
            username=user.username,
            email=user.email.lower(),
            password=hashed_password(user.password),
            phonenumber=user.phonenumber,
            role=user.role,
            status=user.status,
        )

        db.add(new_user)

        db.commit()
        db.refresh(new_user)

        return JSONResponse(
            status_code=201, content={"success": True, "message": "User registered"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(email=user.email).first()
        if not existing_user:
            return JSONResponse(status_code=400, content={"success": False, "message": "Invalid details"})
        if existing_user.status == Status.banned:
            return JSONResponse(status_code=403, content={"success": False, "message": "Your account is banned. Please contact support."})
        if not verify_password(user.password, existing_user.password):
            return JSONResponse(status_code=400, content={"success": False, "message": "Invalid details"})
        access_token = create_access_token(
            data={"sub": existing_user.email, "role": existing_user.role}
        )
        refresh_token = create_refresh_token(
            data={"sub": existing_user.email, "role": existing_user.role}
        )
        existing_user.refresh_token = refresh_token
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "id": existing_user.id,
                    "username": existing_user.username,
                    "email": existing_user.email,
                    "phonenumber": existing_user.phonenumber,
                    "role": existing_user.role,
                },
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh-token")
async def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_refresh_token(request.refresh_token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        existing_user = db.query(User).filter_by(email=user_email).first()
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        if existing_user.refresh_token != request.refresh_token:
            raise HTTPException(
                status_code=401, detail="Invalid or revoked refresh token"
            )
        access_token = create_access_token(
            data={"sub": existing_user.email, "role": existing_user.role}
        )
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/request-password-reset")
async def request_password_reset(user: EmailRequest, db: Session = Depends(get_db)):
    exisitng_user = db.query(User).filter_by(email=user.email).first()
    if not exisitng_user:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"message": "Email verified. Proceed to reset password."}


@router.post("/reset-password")
async def reset_password(user: PasswordResetRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(email=user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found")
    if not user.new_password:
        raise HTTPException(status_code=400, detail="New password is required")
    if verify_password(user.new_password, existing_user.password):
        raise HTTPException(
            status_code=400,
            detail="New password cannot be the same as the old password",
        )
    existing_user.password = hashed_password(user.new_password)
    db.add(existing_user)
    db.commit()
    db.refresh(existing_user)
    return {"message": "Password updated successfully"}


# only admins has access to get all users
@router.get(
    "/get-users", response_model=list[UserOut], summary="Get all users (admin only)"
)
async def get_all_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )
    try:
        users = db.query(User).all()
        if not users:
            return JSONResponse(
                status_code=404, content={"success": False, "message": "No users found"}
            )
        return users
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while fetching users: {str(e)}"
        )


# admin can update user details by role or status
@router.patch("/toggle-status", summary="Update user details(admin only)")
async def toggle_user_status(
    toggle_user: toggleStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )
    existing_user = db.query(User).filter(User.id == toggle_user.id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if toggle_user.role is not None and toggle_user.role not in [role.value for role in RoleEnum]:
        raise HTTPException(status_code=400, detail="Invalid role")
    if toggle_user.role is not None and toggle_user.status not in [status.value for status in Status]:
        raise HTTPException(status_code=400, detail="Invalid status")
    if existing_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot change your own role or status.")
    
    try:
        if toggle_user.role is not None:
            existing_user.role = toggle_user.role
        if toggle_user.status is not None:
            existing_user.status = toggle_user.status
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "User details updated successfully",
                "user": {
                    "id": existing_user.id,
                    "username": existing_user.username,
                    "email": existing_user.email,
                    "role": existing_user.role,
                    "status": existing_user.status,
                },
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating user details: {str(e)}",
        )


# edit user details
@router.patch("/update-user", summary="Update user details")
async def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user.id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this user."
        )
    existing_user = db.query(User).filter(User.id == user.id).first()
    try:
        if user.username is not None:
            existing_user.username = user.username
        if user.email is not None:
            existing_user.email = user.email.lower()
        if user.phonenumber is not None:
            existing_user.phonenumber = user.phonenumber

        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "User details updated successfully",
                "user": {
                    "id": existing_user.id,
                    "username": existing_user.username,
                    "email": existing_user.email,
                    "phonenumber":existing_user.phonenumber,
                    "role": existing_user.role,
                    "status": existing_user.status,
                },
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating user details: {str(e)}",
        )
    
#get user by id
@router.get("/get-user/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403, detail="You do not have permission to view this user."
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
