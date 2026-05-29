from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str


class NoteOut(BaseModel):
    id: int
    ticket_id: str
    note_text: str
    created_at: datetime

    class Config:
        from_attributes = True


class TicketOut(BaseModel):
    id: int
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TicketDetail(TicketOut):
    notes: List[NoteOut] = []


class TicketUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None
