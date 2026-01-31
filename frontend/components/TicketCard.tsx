import Link from 'next/link';
import { formatDistanceToNow } from 'date-fns';
import { Ticket } from '@/types/ticket';
import { UrgencyBadge, StatusBadge, CategoryBadge } from './StatusBadge';

interface Props {
  ticket: Ticket;
}

export function TicketCard({ ticket }: Props) {
  const urgencyBorder = {
    high: 'border-l-red-500',
    medium: 'border-l-yellow-500',
    low: 'border-l-green-500',
  };

  return (
    <Link href={`/tickets/${ticket.id}`}>
      <div
        className={`p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow border-l-4 ${
          ticket.urgency ? urgencyBorder[ticket.urgency] : 'border-l-gray-300'
        }`}
      >
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-medium text-gray-900 truncate flex-1">
            {ticket.subject}
          </h3>
          <StatusBadge status={ticket.status} />
        </div>

        <p className="text-sm text-gray-600 mb-3">
          {ticket.customer_name} • {ticket.customer_email}
        </p>

        <div className="flex items-center gap-2 flex-wrap">
          <UrgencyBadge urgency={ticket.urgency} />
          <CategoryBadge category={ticket.category} />
          <span className="text-xs text-gray-400 ml-auto">
            {formatDistanceToNow(new Date(ticket.created_at), { addSuffix: true })}
          </span>
        </div>
      </div>
    </Link>
  );
}