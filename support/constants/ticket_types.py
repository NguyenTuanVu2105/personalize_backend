class SupportTicketType:
    ORDER = '2'
    PRODUCT = '3'


class VerboseSupportTicketType:
    ORDER = 'order'
    PRODUCT = 'product'


SUPPORT_TICKET_TYPES = [
    (SupportTicketType.ORDER, VerboseSupportTicketType.ORDER),
    (SupportTicketType.PRODUCT, VerboseSupportTicketType.PRODUCT),
]

SUPPORT_TICKET_TYPE_VERBOSE_DICT = {verbose: status for status, verbose in SUPPORT_TICKET_TYPES}
SUPPORT_TICKET_TYPE_DICT = {status: verbose for status, verbose in SUPPORT_TICKET_TYPES}
