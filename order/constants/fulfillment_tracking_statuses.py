class FulfilmentOrderPackTrackingStatus:
    UNKNOWN = "1"
    PRE_TRANSIT = "2"
    IN_TRANSIT = "3"
    OUT_FOR_DELIVERY = "4"
    DELIVERED = "5"
    AVAILABLE_FOR_PICKUP = "6"
    RETURN_TO_SENDER = "7"
    FAILURE = "8"
    CANCELLED = "9"
    ERROR = "10"


class VerboseFulfilmentOrderPackTrackingStatus:
    UNKNOWN = "unknown"
    PRE_TRANSIT = "pre_transit"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    AVAILABLE_FOR_PICKUP = "available_for_pickup"
    RETURN_TO_SENDER = "return_to_sender"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    ERROR = "error"


FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES = (
    (FulfilmentOrderPackTrackingStatus.UNKNOWN, VerboseFulfilmentOrderPackTrackingStatus.UNKNOWN),
    (FulfilmentOrderPackTrackingStatus.PRE_TRANSIT, VerboseFulfilmentOrderPackTrackingStatus.PRE_TRANSIT),
    (FulfilmentOrderPackTrackingStatus.IN_TRANSIT, VerboseFulfilmentOrderPackTrackingStatus.IN_TRANSIT),
    (FulfilmentOrderPackTrackingStatus.OUT_FOR_DELIVERY, VerboseFulfilmentOrderPackTrackingStatus.OUT_FOR_DELIVERY),
    (FulfilmentOrderPackTrackingStatus.DELIVERED, VerboseFulfilmentOrderPackTrackingStatus.DELIVERED),
    (FulfilmentOrderPackTrackingStatus.AVAILABLE_FOR_PICKUP,
     VerboseFulfilmentOrderPackTrackingStatus.AVAILABLE_FOR_PICKUP),
    (FulfilmentOrderPackTrackingStatus.RETURN_TO_SENDER, VerboseFulfilmentOrderPackTrackingStatus.RETURN_TO_SENDER),
    (FulfilmentOrderPackTrackingStatus.FAILURE, VerboseFulfilmentOrderPackTrackingStatus.FAILURE),
    (FulfilmentOrderPackTrackingStatus.CANCELLED, VerboseFulfilmentOrderPackTrackingStatus.CANCELLED),
    (FulfilmentOrderPackTrackingStatus.ERROR, VerboseFulfilmentOrderPackTrackingStatus.ERROR)
)

FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT = {status: verbose for status, verbose in
                                               FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES}
FULFILLMENT_ORDER_PACK_TRACKING_STATUSES_NEED_TO_UPDATE = [FulfilmentOrderPackTrackingStatus.UNKNOWN,
                                                           FulfilmentOrderPackTrackingStatus.PRE_TRANSIT,
                                                           FulfilmentOrderPackTrackingStatus.IN_TRANSIT,
                                                           FulfilmentOrderPackTrackingStatus.OUT_FOR_DELIVERY,
                                                           FulfilmentOrderPackTrackingStatus.AVAILABLE_FOR_PICKUP,
                                                           FulfilmentOrderPackTrackingStatus.RETURN_TO_SENDER]
# ORDER_PACK_TRACKING_STATUS_NEED_TO_UPDATE = [OrderPackTrackingStatus.UNKNOWN,
#                                              OrderPackTrackingStatus.PRE_TRANSIT,
#                                              OrderPackTrackingStatus.IN_TRANSIT,
#                                              OrderPackTrackingStatus.OUT_FOR_DELIVERY,
#                                              OrderPackTrackingStatus.DELIVERED,
#                                              OrderPackTrackingStatus.AVAILABLE_FOR_PICKUP,
#                                              OrderPackTrackingStatus.RETURN_TO_SENDER,
#                                              OrderPackTrackingStatus.FAILURE,
#                                              OrderPackTrackingStatus.CANCELLED,
#                                              OrderPackTrackingStatus.ERROR]
FULFILLMENT_ORDER_PACK_TRACKING_STATUS_VERBOSE_DICT = {verbose: status for status, verbose in FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES}
FULFILLMENT_ORDER_PACK_TRACKING_STATUS_DICT = {status: verbose for status, verbose in FULFILLMENT_ORDER_PACK_TRACKING_STATUS_CHOICES}
