from django.apps import AppConfig


class StripePaymentConfig(AppConfig):
    name = 'billing.sub_apps.stripe_payment'

    def ready(self):
        import billing.sub_apps.stripe_payment.signals
