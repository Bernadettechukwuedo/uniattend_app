from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    organizer = "organizer"
    admin = "admin"

class Status(str, Enum):
    active = "active" 
    banned = "banned"

class toggleStatus(BaseModel):
    id:int
    role: RoleEnum | None = None
    status: Status | None = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phonenumber: str
    role: RoleEnum = RoleEnum.student
    status: Status = Status.active

class UserUpdate(BaseModel):
    id: int
    username: str | None = None
    email: EmailStr | None = None
    phonenumber: str | None = None


class UserOut(BaseModel):
   id: int
   username: str
   email: EmailStr
   role: RoleEnum
   status: Status
   phonenumber:str
   
   

   class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailRequest(BaseModel):
    email: EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr
    new_password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str

class EventCreate(BaseModel):
    name: str
    description: str | None = None
    date: str  # Format: YYYY-MM-DD
    time:str
    location: str 
    capacity: int 
    organizer: str
    image: str | None = None 

class EventUpdate(BaseModel):
    id: int
    name: str | None = None
    description: str | None = None
    date: str | None = None
    time: str | None = None
    location: str | None = None
    capacity: int | None = None
    organizer: str | None = None
    image: str | None = None  # Assuming you want to update the image filename

class EventOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    date: str  # Format: YYYY-MM-DD
    time: str 
    location: str 
    capacity: int 
    created_by: int
    organizer: str
    image: str | None = None 

    class Config:
        from_attributes = True

class RegisterSchema(BaseModel):
    user_id: int
    event_id:int

class RegisterOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    registration_date: str  # Format: YYYY-MM-DD
    checked_in : bool

    class Config:
        from_attributes = True

class StudentEventRegistrationOut(BaseModel):
    total: int
    registrations: list[RegisterOut]
    
class StudentRegistrationOut(BaseModel):
    event_id:int
    user_id: int
    name: str
    organizer: str
    description:str
    capacity:int
    location:str
    date:str
    time:str
    image:str
    qr_code_path:str
    registration_date: str  # Format: YYYY-MM-DD
class StudentRegistrationCount(BaseModel):
    total: int
    registrations: list[StudentRegistrationOut]

class QRCheckIn(BaseModel):
    qr_data: str


class PaginatedEventResponse(BaseModel):
    success: bool
    total: int
    limit: int
    offset: int
    events: list[EventOut]

class EventListResponse(BaseModel):
    success: bool
    total: int
    events: list[EventOut]

class GetAllReg(BaseModel):
    user_id: int
    registration_date: str  # Format: YYYY-MM-DD
    checked_in : bool
    class Config:
        from_attributes = True
