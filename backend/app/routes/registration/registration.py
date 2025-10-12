from fastapi import APIRouter, Depends, HTTPException, UploadFile
from app.models import Event, User, RoleEnum, Registration
from app.routes.auth.auth_utils import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime
from app.schemas import (
    RegisterSchema,
    RegisterOut,
    StudentRegistrationOut,
    QRCheckIn,
    StudentRegistrationCount,
    StudentEventRegistrationOut,
    GetAllReg,
)
import qrcode
import os
from uuid import uuid4
from fastapi.responses import JSONResponse


# add email technology to send qr code to the users email
# admin to view all registered users
router = APIRouter(prefix="/registration", tags=["registrations"])


# register for an event
@router.post("/register-event", summary="Register for an event")
async def register_event(
    registration: RegisterSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role in [RoleEnum.organizer, RoleEnum.admin]:
        raise HTTPException(
            status_code=403, detail="You are not allowed to register for an event"
        )
    if registration.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Invalid user")
    event = db.query(Event).filter(Event.id == registration.event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if datetime.strptime(event.date, "%Y-%m-%d") < datetime.now():
        raise HTTPException(status_code=400, detail="You cant register for past event")
    existing_registration = (
        db.query(Registration)
        .filter(
            Registration.user_id == registration.user_id,
            Registration.event_id == registration.event_id,
        )
        .first()
    )
    if existing_registration:
        raise HTTPException(
            status_code=400, detail="You are already registered for this event"
        )
    if event.capacity == 0:
        raise HTTPException(status_code=400, detail="Event is full")
    try:
        qr_content = f"{current_user.id}--{event.id}--{str(uuid4())}"
        qr = qrcode.make(qr_content)

        qr_filename = f"{current_user.id}_{event.id}_{uuid4().hex}.png"
        qr_folder = "static/qrcodes"
        os.makedirs(qr_folder, exist_ok=True)
        qr_path = os.path.join(qr_folder, qr_filename)
        qr.save(qr_path)

        event.capacity -= 1
        new_registration = Registration(
            user_id=current_user.id, event_id=event.id, qr_code_path=qr_filename
        )
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)

        return {
            "success": True,
            "message": "Registered successfully",
            "registration_id": new_registration.id,
            "qr_code_path": new_registration.qr_code_path,
            "qr_code_url": f"/static/qrcodes/{qr_filename}",
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to register for event:{str(e)}"
        )


# unregister for an event
@router.delete("/unregister", summary="Unregister an event")
async def unregister_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        registration = (
            db.query(Registration)
            .filter(
                Registration.user_id == current_user.id,
                Registration.event_id == event_id,
            )
            .first()
        )
        if not registration:
            raise HTTPException(
                status_code=404, detail="You are not registered for this event"
            )
        if registration.qr_code_path:
            qr_path = os.path.join("static", "qrcodes", registration.qr_code_path)
            if os.path.exists(qr_path):
                os.remove(qr_path)

        db.delete(registration)
        event.capacity += 1
        db.commit()
        return JSONResponse(
            status_code=201,
            content={"success": True, "message": "Unregistered successfully"},
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to unregister for event:{str(e)}"
        )


# only admins has access to get all registrations
@router.get(
    "/get-registration",
    response_model=list[GetAllReg],
    summary="Get all registrations (admin only)"
)
async def get_all_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource."
        )

    try:
        registrations = db.query(Registration).all()

        result = []
        for reg in registrations:
            result.append(
                GetAllReg(
                    user_id=reg.user_id,
                    registration_date=reg.registration_date.strftime("%Y-%m-%d"),
                    checked_in=reg.checked_in,
                )
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching registrations: {str(e)}"
        )


# organizes can view all students that registered for their event
@router.get(
    "/view-all-student-registrations",
    response_model=StudentEventRegistrationOut,
    summary="View all student registrations",
)
async def view_all_student_registrations(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != RoleEnum.organizer:
            raise HTTPException(
                status_code=403, detail="You are not authorized to view this event"
            )
        events = db.query(Event).filter(Event.created_by == current_user.id).all()
        if not events:
            raise HTTPException(status_code=404, detail="No events found")

        result = []
        total = 0
        for event in events:
            registrations = (
                db.query(Registration).filter(Registration.event_id == event.id).all()
            )
            total += len(registrations)
            for reg in registrations:
                result.append(
                    RegisterOut(
                        user_id=reg.user_id,
                        username=reg.user.username,
                        email=reg.user.email,
                        registration_date=reg.registration_date.strftime("%Y-%m-%d"),
                        checked_in=reg.checked_in,
                    )
                )
        return {"total": total, "registrations": result}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to view student registrations:{str(e)}"
        )


# organizers can view students that registers for their event
@router.get(
    "/view-student-registrations",
    response_model=list[RegisterOut],
    summary="View student registrations",
)
async def view_student_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event.created_by != current_user.id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to view this event"
            )
        registrations = (
            db.query(Registration).filter(Registration.event_id == event_id).all()
        )
        if not registrations:
            raise HTTPException(status_code=404, detail="No registrations found")

        result = []
        for reg in registrations:
            result.append(
                RegisterOut(
                    user_id=reg.user_id,
                    username=reg.user.username,
                    email=reg.user.email,
                    registration_date=reg.registration_date.strftime("%Y-%m-%d"),
                    checked_in=reg.checked_in,
                )
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to view student registrations:{str(e)}"
        )
#get users registeration using user id
@router.get(
    "/get-registrations/{user_id}",
    response_model=StudentRegistrationCount,
    summary="View registered events",
)
async def get_registrations(
    user_id:int,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    try:
        if current_user.role != RoleEnum.admin :
            raise HTTPException(
                status_code=403, detail="You are not authorized to view this event"
            )
        registrations = (
            db.query(Registration).filter(Registration.user_id == user_id).all()
        )
        total = len(registrations)


        result = []
        for reg in registrations:
            result.append(
                StudentRegistrationOut(
                    event_id=reg.event.id,
                    user_id=reg.user_id,
                    name=reg.event.name,
                    organizer=reg.event.organizer,
                    description=reg.event.description,
                    capacity=reg.event.capacity,
                    location=reg.event.location,
                    date=reg.event.date,
                    time=reg.event.time,
                    image=reg.event.image,
                    qr_code_path=reg.qr_code_path,
                    registration_date=reg.registration_date.strftime("%Y-%m-%d"),
                )
            )
        return {"total": total, "registrations": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to view registrations:{str(e)}"
        )

# user can view their registrations
@router.get(
    "/get-registrations",
    response_model=StudentRegistrationCount,
    summary="View registered events",
)
async def get_registrations(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        if current_user.role != RoleEnum.student :
            raise HTTPException(
                status_code=403, detail="You are not authorized to view this event"
            )
        registrations = (
            db.query(Registration).filter(Registration.user_id == current_user.id).all()
        )
        total = len(registrations)


        result = []
        for reg in registrations:
            result.append(
                StudentRegistrationOut(
                    event_id=reg.event.id,
                    user_id=reg.user_id,
                    name=reg.event.name,
                    organizer=reg.event.organizer,
                    description= reg.event.description,
                    capacity=reg.event.capacity,
                    location=reg.event.location,
                    date=reg.event.date,
                    time=reg.event.time,
                    image=reg.event.image,
                    qr_code_path=reg.qr_code_path,
                    registration_date=reg.registration_date.strftime("%Y-%m-%d"),
                )
            )
        return {"total": total, "registrations": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to view registrations:{str(e)}"
        )




# checking qr code
@router.post("/validate-qr")
async def validate_qr(
    qr_code: QRCheckIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        qr_data = qr_code.qr_data
        user_id, event_id, _ = qr_data.split("--")
        user_id = int(user_id)
        event_id = int(event_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid QR format")

    registration = (
        db.query(Registration).filter_by(user_id=user_id, event_id=event_id).first()
    )
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    event = db.query(Event).filter_by(id=event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if current_user.id != event.created_by:
        raise HTTPException(status_code=403, detail="Unauthorized check-in attempt")

    today = datetime.now().date()
    event_date = datetime.strptime(event.date, "%Y-%m-%d").date()
    if today != event_date:
        raise HTTPException(
            status_code=400, detail="Check-in allowed only on the event date"
        )

    if registration.checked_in:
        raise HTTPException(status_code=400, detail="Attendee has already checked in")

    registration.checked_in = True
    db.commit()

    return {
        "success": True,
        "message": "Check-in successful",
        "attendee_id": registration.user_id,
        "event_id": registration.event_id,
    }
