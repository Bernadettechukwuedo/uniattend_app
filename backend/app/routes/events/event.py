from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile
from app.schemas import EventOut, PaginatedEventResponse,EventListResponse
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime
from fastapi.responses import JSONResponse
from app.models import Event, User, RoleEnum
from app.routes.auth.auth_utils import get_current_user
from cloudinary.uploader import upload, destroy



router = APIRouter(prefix="/events", tags=["Events"])


# create an event
@router.post("/create-event", summary="Create a new event")
async def create_event(
    name: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),  # Format: YYYY-MM-DD
    time: str = Form(...),  # Format: HH:MM
    location: str = Form(...),
    capacity: int = Form(..., ge=1),  # Ensure capacity is a positive integer
    organizer: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("Image filename:", image.filename)
    if current_user.role != RoleEnum.organizer:
        raise HTTPException(
            status_code=403, detail="You do not have permission to create events."
        )
    if not name or not date or not location or not organizer:
        raise HTTPException(status_code=400, detail="All fields are required.")
    if capacity <= 0:
        raise HTTPException(
            status_code=400, detail="Capacity must be a positive integer."
        )
    try:
        # Validate date format
        event_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Date must be in YYYY-MM-DD format."
        )
    try:
        event_time = datetime.strptime(time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Time must be in HH:MM format.")

    event_datetime = datetime.combine(event_date.date(), event_time)
    if event_datetime <= datetime.now():
        raise HTTPException(
            status_code=400, detail="Event must be scheduled in the future."
        )
    try:
        contents = await image.read()
        
        # Upload to Cloudinary
        upload_result = upload(contents, folder="events", resource_type="image")
        image_url = upload_result.get("secure_url")

        new_event = Event(
            name=name,
            date=date,
            time=time,
            location=location,
            organizer=organizer,
            capacity=capacity,
            created_by=current_user.id,
            description=description,
            image=image_url,  # Assuming you want to save the image filename
        )
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "Event created successfully",
                "event": {
                    "id": new_event.id,
                    "name": new_event.name,
                    "date": new_event.date,
                    "time": new_event.time,
                    "location": new_event.location,
                    "organizer": new_event.organizer,
                    "capacity": new_event.capacity,
                    "created_by": new_event.created_by,
                    "description": new_event.description,
                    "image": image_url,  
                },
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the event: {str(e)}",
        )


# get all events or use search keyword to get specific event
@router.get(
    "/get-events", response_model=PaginatedEventResponse, summary="Get all events"
)
async def get_events(
    search: str | None = Query(
        None, description="Search keyword for event name or description or user"
    ),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Event).join(Event.creator)
        if search:
            offset = 0
            query = query.filter(
                Event.name.ilike(f"%{search}%")
                | Event.description.ilike(f"%{search}%")
                | Event.organizer.ilike(f"%{search}%")
                | User.username.ilike(f"%{search}%")
            )

        total = query.count()
        events = query.order_by(Event.date.desc()).offset(offset).limit(limit).all()
        return {
            "success": True,
            "total": total,
            "limit": limit,
            "offset": offset,
            "events": events,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500, detail=f"An error occurred while fetching events: {str(e)}"
        )


# edit event details
@router.patch("/update-events", summary="Update events")
async def update_events(
    id: int = Form(...),
    name: str | None = Form(None),
    description: str | None = Form(None),
    location: str | None = Form(None),
    capacity: int | None = Form(None),
    date: str | None = Form(None),
    organizer: str | None = Form(None),
    time: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != RoleEnum.organizer:
        raise HTTPException(
            status_code=403, detail="You do not have permission to create events."
        )
    existing_event = db.query(Event).filter(Event.id == id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    if existing_event.created_by != current_user.id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this event."
        )

    try:

        if name is not None:
            existing_event.name = name
        if location is not None:
            existing_event.location = location
        if organizer is not None:
            existing_event.organizer = organizer
        if capacity is not None:
            existing_event.capacity = capacity
        if description is not None:
            existing_event.description = description
        if date is not None:
            existing_event.date = date
        if time is not None:
            existing_event.time = time
        if image is not None:
            # Delete old Cloudinary image if exists
            if existing_event.image and "res.cloudinary.com" in existing_event.image:
                public_id = "/".join(existing_event.image.split("/")[-2:]).split(".")[0]
                try:
                    destroy(public_id)
                except Exception as e:
                    print(f"Failed to delete old image: {e}")

            contents = await image.read()
            upload_result = upload(contents, folder="events", resource_type="image")
            existing_event.image = upload_result["secure_url"]

        db.commit()
        db.refresh(existing_event)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Event updated successfully",
                "event": {
                    "id": existing_event.id,
                    "name": existing_event.name,
                    "date": existing_event.date,
                    "location": existing_event.location,
                    "organizer": existing_event.organizer,
                    "capacity": existing_event.capacity,
                    "description": existing_event.description,
                    "image": existing_event.image,
                },
            },
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"An error occurred while updating the event: {str(e)}"},
        )
# delete events
@router.delete("/delete-event/{event_id}", summary="Delete an event")
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_event = db.query(Event).filter(Event.id == event_id).first()
    if not existing_event:
        return JSONResponse(status_code=404, content={"success": False, "message": "Event not found."})
    if (
        existing_event.created_by == current_user.id
        or current_user.role == RoleEnum.admin
    ):

        try:
                        # Delete image from Cloudinary if it's a Cloudinary URL
            if existing_event.image and "res.cloudinary.com" in existing_event.image:
                public_id = "/".join(existing_event.image.split("/")[-2:]).split(".")[0]
                try:
                    destroy(public_id)
                except Exception as e:
                    print(f"Failed to delete image from Cloudinary: {e}")

            db.delete(existing_event)
            db.commit()
            return JSONResponse(
                status_code=200,
                content={"success": True, "message": "Event deleted successfully"},
            )
        except Exception as e:
            db.rollback()
            return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"An error occurred while deleting the event: {str(e)}"},
)

    else:
        return JSONResponse(
            status_code=403, content={"success": False, "message": "You do not have permission to delete this event."}
        )

#list event based on the organizerid
@router.get(
    "/organizer-event/{organizer_id}",
    response_model=EventListResponse,
    summary="Get events based on the organizer",
)
async def get_event_by_organizerid(
    organizer_id: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:

        if current_user.role != RoleEnum.admin:
            return JSONResponse(
                status_code=403,
                detail="You do not have permission to access this endpoint",
            )
        get_event= db.query(Event).filter(Event.created_by == organizer_id)
        events = get_event.all()
        total = get_event.count()
        
        return {
            "success": True,
            "total": total,
            "events": events,
        }
        

    except Exception as e:
        return JSONResponse(
            status_code=500,
            detail=f"An error occurred while getting the event:{str(e)}",
        )


# list event based on the organizer
@router.get(
    "/organizer-event",
    response_model=PaginatedEventResponse,
    summary="Get events based on the organizer",
)
async def get_event_by_organizer(
        search: str | None = Query(
        None, description="Search keyword for event name or description or user"
    ),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        if current_user.role != RoleEnum.organizer:
            return JSONResponse(
                status_code=403,
                detail="You do not have permission to access this endpoint",
            )
        query = db.query(Event)
        if search:
            offset = 0
            query = query.filter(
                Event.name.ilike(f"%{search}%")
                | Event.description.ilike(f"%{search}%")
            )

    
        get_event = query.filter(Event.created_by == current_user.id).offset(offset).limit(limit).all()
        total= len(get_event)
        return {
            "success": True,
            "total": total,
            "limit": limit,
            "offset": offset,
            "events": get_event,
        }
        

    except Exception as e:
        return JSONResponse(
            status_code=500,
            detail=f"An error occurred while getting the event:{str(e)}",
        )
#get event details based on event id
@router.get("/event-details/{event_id}", response_model=EventOut, summary="Get event details by ID")
async def get_event_details(
    event_id: int,
    db: Session = Depends(get_db)
):
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Event not found"},
            )
        return event
    except Exception as e:
        return JSONResponse(
            status_code=500,
            detail=f"An error occurred while fetching event details: {str(e)}"
        )
