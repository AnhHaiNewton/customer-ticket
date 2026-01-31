# services/ticket_worker.py
import json
import time
import traceback
from db import redis_client, Session
from models.ticket import Ticket, TicketStatus
from services.ai_triage import triage_ticket

QUEUE_NAME = "ticket_triage_queue"

def enqueue_ticket(ticket_id: str):
    """Add ticket to processing queue"""
    redis_client.rpush(QUEUE_NAME, ticket_id)
    print(f"[QUEUE] Enqueued ticket: {ticket_id}")

def process_single_ticket(ticket_id: str):
    """Process a single ticket with AI triage"""
    with Session() as session:
        ticket = session.query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            print(f"[WORKER] Ticket not found: {ticket_id}")
            return
        
        if ticket.status != TicketStatus.PENDING:
            print(f"[WORKER] Ticket already processed: {ticket_id}")
            return
        
        # Update status to processing
        ticket.status = TicketStatus.PROCESSING
        session.commit()
        
        try:
            # Call AI
            result = triage_ticket(
                customer_name=ticket.customer_name,
                subject=ticket.subject,
                message=ticket.message
            )
            
            # Update ticket with AI results
            ticket.category = result.category
            ticket.sentiment_score = result.sentiment_score
            ticket.urgency = result.urgency
            ticket.ai_draft_response = result.draft_response
            ticket.status = TicketStatus.PROCESSED
            session.commit()
            
            print(f"[WORKER] Processed ticket: {ticket_id} -> {result.category}, {result.urgency}")
            
        except Exception as e:
            print(f"[WORKER] Error processing ticket {ticket_id}: {e}")
            traceback.print_exc()
            ticket.status = TicketStatus.FAILED
            session.commit()

def run_worker():
    """Main worker loop"""
    print("[WORKER] Starting ticket triage worker...")
    print(f"[WORKER] Listening on queue: {QUEUE_NAME}")
    
    while True:
        try:
            # Blocking pop - wait for new tickets
            result = redis_client.blpop(QUEUE_NAME, timeout=5)
            
            if result:
                _, ticket_id = result
                ticket_id = ticket_id.decode('utf-8')
                print(f"[WORKER] Received ticket: {ticket_id}")
                process_single_ticket(ticket_id)
                
        except Exception as e:
            print(f"[WORKER] Error: {e}")
            traceback.print_exc()
            time.sleep(1)

if __name__ == "__main__":
    run_worker()