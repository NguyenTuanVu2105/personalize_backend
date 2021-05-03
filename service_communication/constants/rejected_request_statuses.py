class RejectedRequestStatus:
    PENDING = "0"
    REJECTED = "1"
    RESOLVED = "2"


class VerboseRejectedRequestStatus:
    PENDING = "pending"
    REJECTED = "rejected"
    RESOLVED = "resolved"


REJECTED_REQUEST_STATUS_CHOICES = [
    (RejectedRequestStatus.PENDING, VerboseRejectedRequestStatus.PENDING),
    (RejectedRequestStatus.REJECTED, VerboseRejectedRequestStatus.REJECTED),
    (RejectedRequestStatus.RESOLVED, VerboseRejectedRequestStatus.RESOLVED)
]
