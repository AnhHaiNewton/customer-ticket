'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, Send, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';
import { Ticket } from '@/types/ticket';
import { ticketApi } from '@/lib/api';
import { UrgencyBadge, StatusBadge, CategoryBadge } from '@/components/StatusBadge';

export default function TicketDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [loading, setLoading] = useState(true);
  const [draftResponse, setDraftResponse] = useState('');
  const [resolving, setResolving] = useState(false);

  const fetchTicket = async () => {
    try {
      const data = await ticketApi.get(params.id as string);
      setTicket(data);
      setDraftResponse(data.ai_draft_response || '');
    } catch (error) {
      console.error('Failed to fetch ticket:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTicket();
  }, [params.id]);

  // Poll if still processing
  useEffect(() => {
    if (ticket?.status === 'pending' || ticket?.status === 'processing') {
      const interval = setInterval(fetchTicket, 3000);
      return () => clearInterval(interval);
    }
  }, [ticket?.status]);

  const handleResolve = async () => {
    if (!draftResponse.trim()) {
      alert('Please enter a response');
      return;
    }

    setResolving(true);
    try {
      await ticketApi.resolve(params.id as string, {
        final_response: draftResponse,
        resolved_by: 'Agent', // Hardcoded for demo
      });
      fetchTicket();
    } catch (error) {
      console.error('Failed to resolve ticket:', error);
      alert('Failed to resolve ticket');
    } finally {
      setResolving(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  if (!ticket) {
    return <div className="text-center py-12">Ticket not found</div>;
  }

  return (
    <div className='text-black'>
      {/* Back button */}
      <button
        onClick={() => router.push('/tickets')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft size={20} />
        Back to tickets
      </button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Ticket Info */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-start justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">{ticket.subject}</h2>
            <StatusBadge status={ticket.status} />
          </div>

          <div className="flex gap-2 mb-4">
            <UrgencyBadge urgency={ticket.urgency} />
            <CategoryBadge category={ticket.category} />
            {ticket.sentiment_score && (
              <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-800">
                Sentiment: {ticket.sentiment_score}/10
              </span>
            )}
          </div>

          <div className="border-t pt-4 space-y-3">
            <div>
              <span className="text-sm text-gray-500">Customer:</span>
              <p className="font-medium">{ticket.customer_name}</p>
              <p className="text-sm text-gray-600">{ticket.customer_email}</p>
            </div>

            <div>
              <span className="text-sm text-gray-500">Message:</span>
              <p className="mt-1 p-3 bg-gray-50 rounded-lg">{ticket.message}</p>
            </div>

            <div className="text-sm text-gray-500">
              Created: {format(new Date(ticket.created_at), 'PPpp')}
            </div>
          </div>
        </div>

        {/* Right: Response */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Response</h3>

          {ticket.status === 'pending' || ticket.status === 'processing' ? (
            <div className="flex items-center gap-3 text-blue-600 py-8 justify-center">
              <RefreshCw className="animate-spin" size={24} />
              <span>AI is analyzing the ticket...</span>
            </div>
          ) : ticket.status === 'resolved' ? (
            <div>
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm text-green-800 font-medium mb-2">
                  ✓ Resolved by {ticket.resolved_by}
                </p>
                <p>{ticket.final_response}</p>
              </div>
              {ticket.resolved_at && (
                <p className="text-sm text-gray-500 mt-2">
                  Resolved at: {format(new Date(ticket.resolved_at), 'PPpp')}
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  AI Draft Response
                </label>
                <textarea
                  rows={6}
                  value={draftResponse}
                  onChange={(e) => setDraftResponse(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="AI response will appear here..."
                />
              </div>

              <button
                onClick={handleResolve}
                disabled={resolving || !draftResponse.trim()}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
              >
                <Send size={20} />
                {resolving ? 'Resolving...' : 'Resolve Ticket'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}