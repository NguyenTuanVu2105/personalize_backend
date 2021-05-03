from django.apps import AppConfig


class PaypalVaultPaymentConfig(AppConfig):
    name = 'billing.sub_apps.paypal_vault_payment'

    def ready(self):
        import billing.sub_apps.paypal_vault_payment.signals
