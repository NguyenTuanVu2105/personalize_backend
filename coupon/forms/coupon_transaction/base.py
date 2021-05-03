from django import forms

from HUB.forms.base import BaseForm
from order.models import Order


class CouponTransactionForm(BaseForm):
    code = forms.CharField()
    order = forms.ModelChoiceField(queryset=None)

    def __init__(self, user, *args, **kwargs):
        assert user
        self.user = user
        self.coupon = None
        self.order = None
        self.transaction_idempotency_key = None

        super().__init__(*args, **kwargs)
        self.fields['order'].queryset = Order.objects.filter_by_user_id(user_id=user.id)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if code:
            code = code.upper()
        return code

    def clean_order(self):
        order_obj = self.cleaned_data["order"]
        if not order_obj.is_coupon_editable:
            raise forms.ValidationError(message="Order is not in coupon-editable state")
        self.order = order_obj
        return order_obj
