class SupportTicketStatus:
    OPEN = '2'
    PENDING = '3'
    RESOLVED = '4'
    CLOSED = '5'


class VerboseSupportTicketStatus:
    OPEN = 'open'
    PENDING = 'pending'
    RESOLVED = 'resolved'
    CLOSED = 'closed'


SUPPORT_TICKET_STATUSES = [
    (SupportTicketStatus.OPEN, VerboseSupportTicketStatus.OPEN),
    (SupportTicketStatus.PENDING, VerboseSupportTicketStatus.PENDING),
    (SupportTicketStatus.RESOLVED, VerboseSupportTicketStatus.RESOLVED),
    (SupportTicketStatus.CLOSED, VerboseSupportTicketStatus.CLOSED),
]


SUPPORT_TICKET_STATUS_VERBOSE_DICT = {verbose: status for status, verbose in SUPPORT_TICKET_STATUSES}
SUPPORT_TICKET_STATUS_DICT = {status: verbose for status, verbose in SUPPORT_TICKET_STATUSES}


