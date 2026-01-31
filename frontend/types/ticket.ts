export type TicketStatus = 'pending' | 'processing' | 'processed' | 'resolved' | 'failed';
export type TicketCategory = 'billing' | 'technical' | 'feature_request';
export type TicketUrgency = 'high' | 'medium' | 'low';

export interface Ticket {
  id: string;
  customer_name: string;
  customer_email: string;
  subject: string;
  message: string;
  status: TicketStatus;
  category: TicketCategory | null;
  sentiment_score: number | null;
  urgency: TicketUrgency | null;
  ai_draft_response: string | null;
  final_response: string | null;
  resolved_at: string | null;
  resolved_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateTicketRequest {
  customer_name: string;
  customer_email: string;
  subject: string;
  message: string;
}

export interface ResolveTicketRequest {
  final_response: string;
  resolved_by: string;
}