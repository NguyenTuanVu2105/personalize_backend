from billing.sub_apps.braintree_payment.braintree_service import braintree_gateway


def create_braintree_customer(user):
    braintree_gateway.customer.create({
        "id": user.id,
        "first_name": user.name,
        "email": user.email
    })
