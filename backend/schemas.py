# backend/schemas.py

from pydantic import BaseModel
from typing import Optional

class TicketBase(BaseModel):
    subject: str
    status: str
    priority: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None

class Ticket(TicketBase):
    id: int
    assignee: Optional[str] = None

    class Config:
        orm_mode: True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    ticket_id: int

class Message(MessageBase):
    id: int

    class Config:
        orm_mode: True
