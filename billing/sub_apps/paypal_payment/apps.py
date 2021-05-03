from django.apps import AppConfig


class PaypalPaymentConfig(AppConfig):
    name = 'billing.sub_apps.paypal_payment'

    def ready(self):
        import billing.sub_apps.paypal_payment.signals