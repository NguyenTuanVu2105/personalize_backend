class MessageStatus:
    UNREAD = "0"
    READ = "1"
    DELETED = "2"


class VerboseMessageStatus:
    UNREAD = "unread"
    READ = "read"
    DELETED = "deleted"


MESSAGE_STATUSES = [
    (MessageStatus.UNREAD, VerboseMessageStatus.UNREAD),
    (MessageStatus.READ, VerboseMessageStatus.READ),
    (MessageStatus.DELETED, VerboseMessageStatus.DELETED)
]

MESSAGE_STATUS_VERBOSE_DICT = {verbose: status for status, verbose in MESSAGE_STATUSES}
MESSAGE_STATUS_DICT = {status: verbose for status, verbose in MESSAGE_STATUSES}
