class UserProductStatus:
    ACTIVE = '1'
    INACTIVE = '2'
    UNUSED = '3'
    ERROR = '4'


class VerboseUserProductStatus:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    UNUSED = 'unused'
    ERROR = 'error'


USER_PRODUCT_STATUS_CHOICES = [
    (UserProductStatus.INACTIVE, VerboseUserProductStatus.INACTIVE),
    (UserProductStatus.ACTIVE, VerboseUserProductStatus.ACTIVE),
    (UserProductStatus.ERROR, VerboseUserProductStatus.ERROR),
    (UserProductStatus.UNUSED, VerboseUserProductStatus.UNUSED)
]

IGNORE_QUERY_STATUSES = [UserProductStatus.UNUSED, UserProductStatus.ERROR]
