# schemas/ticket.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional
from models.ticket import TicketStatus, TicketCategory, TicketUrgency

# Request schemas
class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    message: str

class TicketResolve(BaseModel):
    final_response: str
    resolved_by: str

class TicketUpdate(BaseModel):
    ai_draft_response: Optional[str] = None
    final_response: Optional[str] = None

# Response schemas
class TicketResponse(BaseModel):
    id: UUID
    customer_name: str
    customer_email: str
    subject: str
    message: str
    status: TicketStatus
    category: Optional[TicketCategory]
    sentiment_score: Optional[int]
    urgency: Optional[TicketUrgency]
    ai_draft_response: Optional[str]
    final_response: Optional[str]
    resolved_at: Optional[datetime]
    resolved_by: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    id: UUID
    customer_name: str
    subject: str
    status: TicketStatus
    category: Optional[TicketCategory]
    urgency: Optional[TicketUrgency]
    created_at: datetime
    
    class Config:
        from_attributes = True

# AI Triage schema
class AITriageResult(BaseModel):
    category: TicketCategory
    sentiment_score: int
    urgency: TicketUrgency
    draft_response: str