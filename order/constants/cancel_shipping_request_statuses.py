class CancelShippingRequestStatus:
    PENDING = "0"
    APPROVED = "1"
    REJECTED = "2"


class VerboseCancelShippingRequestStatus:
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


CANCEL_SHIPPING_REQUEST_STATUS_CHOICES = (
    (CancelShippingRequestStatus.PENDING, VerboseCancelShippingRequestStatus.PENDING),
    (CancelShippingRequestStatus.APPROVED, VerboseCancelShippingRequestStatus.APPROVED),
    (CancelShippingRequestStatus.REJECTED, VerboseCancelShippingRequestStatus.REJECTED)
)
