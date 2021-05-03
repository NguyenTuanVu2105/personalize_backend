class EventTemplateStatus:
    ACTIVE = '1'
    INACTIVE = '2'


class VerboseEventTemplateType:
    ACTIVE = 'active'
    INACTIVE = 'inactive'


EVENT_TEMPLATE_STATUS = [
    (EventTemplateStatus.ACTIVE, VerboseEventTemplateType.ACTIVE),
    (EventTemplateStatus.INACTIVE, VerboseEventTemplateType.INACTIVE),
]

EVENT_TEMPLATE_STATUS_VERBOSE_DICT = {verbose: status for status, verbose in EVENT_TEMPLATE_STATUS}
EVENT_TEMPLATE_STATIC_DICT = {status: verbose for status, verbose in EVENT_TEMPLATE_STATUS}
