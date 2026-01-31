# controllers/ticket.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session as DBSession
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from db import Session
from models.ticket import Ticket, TicketStatus, TicketUrgency
from schemas.ticket import (
    TicketCreate, 
    TicketResponse, 
    TicketListResponse,
    TicketResolve,
    TicketUpdate
)
from services.ticket_worker import enqueue_ticket

router = APIRouter(prefix="/tickets", tags=["Tickets"])

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.post("", status_code=201, response_model=TicketResponse)
def create_ticket(data: TicketCreate, db: DBSession = Depends(get_db)):
    """Create a new ticket and queue for AI processing"""
    ticket = Ticket(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        subject=data.subject,
        message=data.message,
        status=TicketStatus.PENDING
    )
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    # Queue for background processing (non-blocking)
    enqueue_ticket(str(ticket.id))
    
    return ticket

@router.get("", response_model=List[TicketListResponse])
def list_tickets(
    status: Optional[TicketStatus] = None,
    urgency: Optional[TicketUrgency] = None,
    db: DBSession = Depends(get_db)
):
    """List all tickets with optional filters"""
    query = db.query(Ticket)
    
    if status:
        query = query.filter(Ticket.status == status)
    if urgency:
        query = query.filter(Ticket.urgency == urgency)
    
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: UUID, db: DBSession = Depends(get_db)):
    """Get ticket details"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: UUID, 
    data: TicketUpdate,
    db: DBSession = Depends(get_db)
):
    """Update ticket draft or response"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if data.ai_draft_response is not None:
        ticket.ai_draft_response = data.ai_draft_response
    if data.final_response is not None:
        ticket.final_response = data.final_response
    
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/resolve", response_model=TicketResponse)
def resolve_ticket(
    ticket_id: UUID,
    data: TicketResolve,
    db: DBSession = Depends(get_db)
):
    """Mark ticket as resolved"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    ticket.final_response = data.final_response
    ticket.resolved_by = data.resolved_by
    ticket.resolved_at = datetime.utcnow()
    ticket.status = TicketStatus.RESOLVED
    
    db.commit()
    db.refresh(ticket)
    return ticket