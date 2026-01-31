import axios from 'axios';
import { Ticket, CreateTicketRequest, ResolveTicketRequest } from '@/types/ticket';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
});

export const ticketApi = {
  list: async (status?: string, urgency?: string): Promise<Ticket[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (urgency) params.append('urgency', urgency);
    
    const { data } = await api.get(`/tickets?${params}`);
    return data;
  },

  get: async (id: string): Promise<Ticket> => {
    const { data } = await api.get(`/tickets/${id}`);
    return data;
  },

  create: async (payload: CreateTicketRequest): Promise<Ticket> => {
    const { data } = await api.post('/tickets', payload);
    return data;
  },

  update: async (id: string, payload: Partial<Ticket>): Promise<Ticket> => {
    const { data } = await api.patch(`/tickets/${id}`, payload);
    return data;
  },

  resolve: async (id: string, payload: ResolveTicketRequest): Promise<Ticket> => {
    const { data } = await api.post(`/tickets/${id}/resolve`, payload);
    return data;
  },
};