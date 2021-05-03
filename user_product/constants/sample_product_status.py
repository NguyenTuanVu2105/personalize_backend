class SampleProductStatus:
    ACTIVE = '1'
    INACTIVE = '2'


class VerboseSampleProductStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'


SAMPLE_PRODUCT_STATUS_CHOICES = [
    (SampleProductStatus.INACTIVE, VerboseSampleProductStatus.INACTIVE),
    (SampleProductStatus.ACTIVE, VerboseSampleProductStatus.ACTIVE),
]
