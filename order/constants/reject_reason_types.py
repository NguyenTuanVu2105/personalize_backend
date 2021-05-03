class RejectReasonType:
    NOT_SUPPORT_SHIPPING = "2"
    FULFILL_REJECTED = "3"


class VerboseRejectReasonType:
    NOT_SUPPORT_SHIPPING = "not_support_shipping"
    FULFILL_REJECTED = "fulfill_rejected"


REJECT_REASON_TYPE_CHOICES = (
    (RejectReasonType.NOT_SUPPORT_SHIPPING, VerboseRejectReasonType.NOT_SUPPORT_SHIPPING),
    (RejectReasonType.FULFILL_REJECTED, VerboseRejectReasonType.FULFILL_REJECTED),
)
