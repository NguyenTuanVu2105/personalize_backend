from django.apps import AppConfig


class BraintreePaymentConfig(AppConfig):
    name = 'billing.sub_apps.braintree_payment'

    def ready(self):
        import billing.sub_apps.braintree_payment.braintree_service
        import billing.sub_apps.braintree_payment.signals
