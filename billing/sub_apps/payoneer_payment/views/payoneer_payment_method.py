import logging

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from billing.sub_apps.combine_payment.functions import create_general_payment_method
from billing.sub_apps.combine_payment.functions.check_max_payment_method import check_max_user_payment_method
from billing.sub_apps.payoneer_payment.models import UserPayoneerPaymentMethod
from billing.sub_apps.payoneer_payment.services.payoneer_auth import get_login_with_payoneer_link, \
    validate_payoneer_verify_code
from billing.sub_apps.payoneer_payment.services.payoneer_sdk import PayoneerService

logger = logging.getLogger(__name__)


class PayoneerPaymentMethodViewSet(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   AuthenticatedGenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPayoneerPaymentMethod.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=UserPayoneerPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        data = request.data
        login_link = get_login_with_payoneer_link(user=request.user, current_shop=data['shop'])
        return Response({"success": True, "login_link": login_link})

    @action(methods=["POST"], detail=False, url_path="activate")
    def activate(self, request, *args, **kwargs):
        request_data = request.data
        payee_id = request_data['payee']
        verify_code = request_data['verify_code']
        user_id = self.request.user.pk
        payment_method = UserPayoneerPaymentMethod.objects.filter(user_id=user_id,
                                                                  payee_id=payee_id).first()
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=UserPayoneerPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        if validate_payoneer_verify_code(payee_id, payment_method, verify_code):
            detail = PayoneerService.get_payee_detail(payee_id)
            if detail["status"] != "ACTIVE":
                return Response({"success": False, "description": "Payee is inactive"})
            email = detail["contact"]["email"]
            exist_method = UserPayoneerPaymentMethod.objects.filter(user_id=user_id, email=email).first()
            if exist_method is not None and exist_method.general_payment_methods.filter(is_active=True).exists():
                PayoneerService.delete_payee(payee_id)
                payment_method.delete()
                return Response({"success": False, "description": "Account existed"})
            payment_method.email = email
            payment_method.type = detail["type"]
            payment_method.detail = detail
            payment_method.save()
            create_general_payment_method(payment_method)
            return Response({"success": True, "description": "Payoneer account has been activated successfully"})
