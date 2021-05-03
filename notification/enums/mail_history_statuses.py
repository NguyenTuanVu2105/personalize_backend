class MailHistoryStatus:
    PENDING = "0"
    SENT = "1"
    ERROR = "2"


class VerboseMailHistoryStatus:
    PENDING = "pending"
    SENT = "sent"
    ERROR = "error"


MAIL_HISTORY_STATUSES = [
    (MailHistoryStatus.PENDING, VerboseMailHistoryStatus.PENDING),
    (MailHistoryStatus.SENT, VerboseMailHistoryStatus.SENT),
    (MailHistoryStatus.ERROR, VerboseMailHistoryStatus.ERROR)
]
