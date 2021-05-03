from rest_framework import mixins
from rest_framework.response import Response

from HUB.viewsets.base import AuthenticatedGenericViewSet
from billing.sub_apps.combine_payment.functions.check_max_payment_method import check_max_user_payment_method
from billing.sub_apps.paypal_payment.models import PaypalPaymentMethod
from billing.sub_apps.paypal_payment.services import PaypalBillingAgreementService


class PaypalPaymentMethodViewSet(mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 AuthenticatedGenericViewSet):
    queryset = PaypalPaymentMethod.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        success = False
        created = False
        request_data = request.data
        agreement_token = request_data.get("agreement_token") or ""
        user_id = request.user.id
        is_max_payment_method = check_max_user_payment_method(user=request.user, payment_model=PaypalPaymentMethod)
        if is_max_payment_method:
            return Response({"success": False, "message": "The payment method exceeded allowed"})
        if agreement_token.strip():
            success, agreement_id, payer_info = PaypalBillingAgreementService.activate(agreement_token)
            if success:
                _, created = PaypalPaymentMethod.objects.update_or_create(user_id=user_id,
                                                                          payer_id=payer_info.get("payer_id"),
                                                                          defaults={
                                                                              "agreement_id": agreement_id,
                                                                              "email": payer_info.get("email"),
                                                                          })
                success = True

        return Response({"success": success, "created": created})
