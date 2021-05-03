from HUB.filters import BaseCreatedTimeFilter
from user.models import User


class UserStatisticFilter(BaseCreatedTimeFilter):
    class Meta:
        model = User
        fields = BaseCreatedTimeFilter.Meta.fields + (
            'account_type', 'is_active', 'is_email_confirmed',
            'is_staff', 'is_superuser', 'is_valid_payment', 'is_test_user')
