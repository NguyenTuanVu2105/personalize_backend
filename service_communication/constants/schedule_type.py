class ScheduleType:
    AUTO_SCAN_SUPPORT_TICKET = "1"
    AUTO_RENEW_PAYPAL_TOKEN = "2"


class VerboseScheduleType:
    AUTO_SCAN_SUPPORT_TICKET = "auto_scan_support_ticket"
    AUTO_RENEW_PAYPAL_TOKEN = "auto_renew_paypal_token"


SCHEDULE_TYPES = [
    (ScheduleType.AUTO_SCAN_SUPPORT_TICKET, VerboseScheduleType.AUTO_SCAN_SUPPORT_TICKET),
    (ScheduleType.AUTO_RENEW_PAYPAL_TOKEN, VerboseScheduleType.AUTO_RENEW_PAYPAL_TOKEN),
]
