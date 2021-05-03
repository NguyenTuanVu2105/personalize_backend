class MappingStatus:
    NOTMAP = "0"
    UNMAPPED = "1"
    MAPPED = "2"


class VerboseMappingStatus:
    NOTMAP = "notmap"
    UNMAPPED = "unmapped"
    MAPPED = "mapped"


MAPPING_STATUS_CHOICES = [
    (MappingStatus.NOTMAP, VerboseMappingStatus.NOTMAP),
    (MappingStatus.UNMAPPED, VerboseMappingStatus.UNMAPPED),
    (MappingStatus.MAPPED, VerboseMappingStatus.MAPPED),
]
