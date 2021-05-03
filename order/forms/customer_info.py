from HUB.forms.base import ModelForm
from order.models import CustomerInfo
from order.models.order_invallid import OrderInvalid


class CustomerInfoForm(ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ["customer_id", "first_name", "last_name", "email", "phone"]