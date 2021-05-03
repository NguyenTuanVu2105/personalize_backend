class PaymentGateway:
    BRAINTREE = '1'
    STRIPE = '2'
    PAYONEER = '3'
    PAYPAL_PRO = '4'
    PAYPAL_VAULT = '5'


class VerbosePaymentGateway:
    STRIPE = "stripe"
    BRAINTREE = "braintree"
    PAYONEER = "payoneer"
    PAYPAL_PRO = "paypal_pro"
    PAYPAL_VAULT = "paypal_vault"


PAYMENT_GATEWAY_CHOICES = [
    (PaymentGateway.STRIPE, VerbosePaymentGateway.STRIPE),
    (PaymentGateway.BRAINTREE, VerbosePaymentGateway.BRAINTREE),
    (PaymentGateway.PAYONEER, VerbosePaymentGateway.PAYONEER),
    (PaymentGateway.PAYPAL_PRO, VerbosePaymentGateway.PAYPAL_PRO),
    (PaymentGateway.PAYPAL_VAULT, VerbosePaymentGateway.PAYPAL_VAULT),
]
