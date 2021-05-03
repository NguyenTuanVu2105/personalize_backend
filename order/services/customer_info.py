from django.core.exceptions import ValidationError

from order.forms import CustomerInfoForm


def update_customer_info(customer_info, request_data):
    form = CustomerInfoForm(instance=customer_info, data=request_data["address"])
    if form.is_valid():
        new_customer_info = form.save()
        return new_customer_info
    else:
        raise ValidationError(code="address", message=form.errors)
