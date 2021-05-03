from HUB.forms.base import ModelForm
from order.models.shipping_address import OrderShippingAddress


class OrderShippingAddressForm(ModelForm):
    class Meta:
        model = OrderShippingAddress
        fields = ["first_name", "last_name", "phone", "address1", "address2", "city",
                  "province", "country", "country_code", "company", "zip"]
        optional_fields = ["company", "address2", "phone"]


class UserOrderShippingAddressForm(OrderShippingAddressForm):
    class Meta(OrderShippingAddressForm.Meta):
        fields = ["first_name", "last_name", "phone", "address1", "address2", "city",
                  "province", "country", "country_code", "company", "zip"]
        optional_fields = ["address2", "phone", "city", "province", "country", "country_code", "company", "zip"]
