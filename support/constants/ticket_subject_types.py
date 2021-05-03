class TicketSubjectType:
    REPLACEMENT_REQUEST = '1'
    CHANGE_SIZE_COLOR = '2'
    CHANGE_ADDRESS = '3'
    ORDER_STATUS = '4'
    OTHER = '5'


class VerboseTicketSubjectType:
    REPLACEMENT_REQUEST = 'Replacement Request'
    CHANGE_SIZE_COLOR = 'Change Size/Color'
    CHANGE_ADDRESS = 'Change Address'
    ORDER_STATUS = 'Order Status'
    OTHER = 'Other (please describe below)'


SUPPORT_TICKET_TYPES = [
    (TicketSubjectType.REPLACEMENT_REQUEST, VerboseTicketSubjectType.REPLACEMENT_REQUEST),
    (TicketSubjectType.CHANGE_SIZE_COLOR, VerboseTicketSubjectType.CHANGE_SIZE_COLOR),
    (TicketSubjectType.CHANGE_ADDRESS, VerboseTicketSubjectType.CHANGE_ADDRESS),
    (TicketSubjectType.ORDER_STATUS, VerboseTicketSubjectType.ORDER_STATUS),
    (TicketSubjectType.OTHER, VerboseTicketSubjectType.OTHER),
]