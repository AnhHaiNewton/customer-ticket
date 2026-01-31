# models/ticket.py
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class TicketStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    RESOLVED = "resolved"
    FAILED = "failed"

class TicketCategory(str, PyEnum):
    BILLING = "billing"
    TECHNICAL = "technical"
    FEATURE_REQUEST = "feature_request"

class TicketUrgency(str, PyEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Customer input
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    
    # AI generated
    status = Column(Enum(TicketStatus), default=TicketStatus.PENDING)
    category = Column(Enum(TicketCategory), nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    urgency = Column(Enum(TicketUrgency), nullable=True)
    ai_draft_response = Column(Text, nullable=True)
    
    # Agent actions
    final_response = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)