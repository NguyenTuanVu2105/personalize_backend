from rest_framework.decorators import action

from HUB.viewsets.base import AdminGenericViewSet
from statistic.filters.user_statistic_filter import UserStatisticFilter
from statistic.services import PotentialCustomersWorkbook
from user.models import User


class UserStatistic(AdminGenericViewSet):
    queryset = User.objects.all().defer('password').filter(is_test_user=False)
    filterset_class = UserStatisticFilter

    @action(methods=['GET'], detail=False, url_path='potential-customers')
    def get_potential_customer_as_xlsx(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        workbook = PotentialCustomersWorkbook(queryset=queryset)
        response = workbook.get_workbook()
        return response
