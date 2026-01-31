import { TicketStatus, TicketUrgency, TicketCategory } from '@/types/ticket';

export function UrgencyBadge({ urgency }: { urgency: TicketUrgency | null }) {
  const config = {
    high: 'bg-red-100 text-red-800 border-red-200',
    medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    low: 'bg-green-100 text-green-800 border-green-200',
  };

  if (!urgency) return null;

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded border ${config[urgency]}`}>
      {urgency.toUpperCase()}
    </span>
  );
}

export function StatusBadge({ status }: { status: TicketStatus }) {
  const config = {
    pending: 'bg-gray-100 text-gray-800',
    processing: 'bg-blue-100 text-blue-800',
    processed: 'bg-purple-100 text-purple-800',
    resolved: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded ${config[status]}`}>
      {status}
    </span>
  );
}

export function CategoryBadge({ category }: { category: TicketCategory | null }) {
  const config = {
    billing: 'bg-orange-100 text-orange-800',
    technical: 'bg-blue-100 text-blue-800',
    feature_request: 'bg-indigo-100 text-indigo-800',
  };

  if (!category) return null;

  const label = category.replace('_', ' ');

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded ${config[category]}`}>
      {label}
    </span>
  );
}