from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional

from database import get_db, Ticket, Note
from schemas import TicketCreate, TicketOut, TicketDetail, TicketUpdate, NoteOut

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


def generate_ticket_id(db: Session) -> str:
    count = db.query(Ticket).count()
    return f"TKT-{str(count + 1).zfill(3)}"

#POST /api/tickets
@router.post("", response_model=dict)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    ticket_id = generate_ticket_id(db)
    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open",
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return {"ticket_id": new_ticket.ticket_id, "created_at": new_ticket.created_at}

#GET /api/tickets
@router.get("", response_model=list[TicketOut])
def list_tickets(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)
    if status and status != "All":
        query = query.filter(Ticket.status == status)
    if search:
        query = query.filter(
            or_(
                Ticket.customer_name.ilike(f"%{search}%"),
                Ticket.customer_email.ilike(f"%{search}%"),
                Ticket.ticket_id.ilike(f"%{search}%"),
                Ticket.subject.ilike(f"%{search}%"),
                Ticket.description.ilike(f"%{search}%"),
            )
        )
    return query.order_by(Ticket.created_at.desc()).all()

#GET /api/tickets/{ticket_id}
@router.get("/{ticket_id}", response_model=TicketDetail)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    notes = db.query(Note).filter(Note.ticket_id == ticket_id).order_by(Note.created_at.asc()).all()
    result = TicketDetail.from_orm(ticket)
    result.notes = [NoteOut.from_orm(n) for n in notes]
    return result

# PUT /api/tickets/{ticket_id}
@router.put("/{ticket_id}", response_model=dict)
def update_ticket(ticket_id: str, update: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if update.status:
        ticket.status = update.status
    ticket.updated_at = datetime.utcnow()
    if update.note and update.note.strip():
        new_note = Note(ticket_id=ticket_id, note_text=update.note.strip())
        db.add(new_note)
    db.commit()
    db.refresh(ticket)
    return {"success": True, "updated_at": ticket.updated_at}
