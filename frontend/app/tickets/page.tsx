'use client';

import { useState, useEffect } from 'react';
import { Plus, RefreshCw } from 'lucide-react';
import { Ticket, TicketStatus, TicketUrgency } from '@/types/ticket';
import { ticketApi } from '@/lib/api';
import { TicketCard } from '@/components/TicketCard';
import { CreateTicketModal } from '@/components/CreateTicketModal';

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [filterStatus, setFilterStatus] = useState<string>('');
  const [filterUrgency, setFilterUrgency] = useState<string>('');

  const fetchTickets = async () => {
    try {
      const data = await ticketApi.list(filterStatus, filterUrgency);
      setTickets(data);
    } catch (error) {
      console.error('Failed to fetch tickets:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, [filterStatus, filterUrgency]);

  // Polling every 5 seconds for updates
  useEffect(() => {
    const interval = setInterval(fetchTickets, 5000);
    return () => clearInterval(interval);
  }, [filterStatus, filterUrgency]);

  return (
    <div className="text-black">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Support Tickets</h2>
        <div className="flex gap-3">
          <button
            onClick={fetchTickets}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded-lg"
          >
            <RefreshCw size={20} />
          </button>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus size={20} />
            New Ticket
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-3 py-2 border rounded-lg bg-white"
        >
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="processed">Processed</option>
          <option value="resolved">Resolved</option>
          <option value="failed">Failed</option>
        </select>

        <select
          value={filterUrgency}
          onChange={(e) => setFilterUrgency(e.target.value)}
          className="px-3 py-2 border rounded-lg bg-white"
        >
          <option value="">All Urgency</option>
          <option value="high">🔴 High</option>
          <option value="medium">🟡 Medium</option>
          <option value="low">🟢 Low</option>
        </select>
      </div>

      {/* Ticket List */}
      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      ) : tickets.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No tickets found. Create one to get started!
        </div>
      ) : (
        <div className="grid gap-4">
          {tickets.map((ticket) => (
            <TicketCard key={ticket.id} ticket={ticket} />
          ))}
        </div>
      )}

      {/* Modal */}
      <CreateTicketModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        onCreated={fetchTickets}
      />
    </div>
  );
}