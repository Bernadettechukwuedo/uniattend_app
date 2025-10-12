from .database import Base
from sqlalchemy import Column, String, Integer, Enum, ForeignKey,Boolean
from sqlalchemy.orm import relationship
import enum 
from sqlalchemy import func, DateTime

class RoleEnum(str,enum.Enum):
    student = "student"
    organizer = "organizer"
    admin = "admin"

class Status(str,enum.Enum):
    active="active"
    banned="banned"


class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    phonenumber = Column(String(15), nullable=True) 
    refresh_token = Column(String(512), nullable=True) 
    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False)
    status =Column(Enum(Status), default=Status.active, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    registrations = relationship("Registration", back_populates="user", cascade="all, delete-orphan")
    event_created = relationship("Event", back_populates="creator", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role})>"

class Event (Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(500), nullable=True)
    date = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False, server_default="00:00")
    location = Column(String(100), nullable=True)
    capacity = Column(Integer, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  
    organizer = Column(String(100), nullable=False)
    image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    creator = relationship("User", back_populates="event_created")
    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name}, date={self.date}, organizer={self.organizer})>"

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer,ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    qr_code_path = Column(String(255), nullable=True) 
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    checked_in = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Registration(id={self.id}, user_id={self.user_id}, event_id={self.event_id}, registration_date={self.registration_date})>"


    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")