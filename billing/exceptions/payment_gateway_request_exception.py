class PaymentRequestException(Exception):
    """"""
    pass


class UnretryablePaymentRequestException(PaymentRequestException):
    """An error occurred => sure that request is failed & cannot recharge again
        e.g: 4xx (401, 403) gateway receive request & declares as error due to request data
        Cannot make request with same idempotency key & request data without error
        More about idempotent request: https://developer.paypal.com/docs/platforms/develop/idempotency/
    """
    pass


class RetryablePaymentRequestException(PaymentRequestException):
    """An error occurred => can retry
       e.g: Network error or has problem in Gateway (5xx),
       Can be resent with same idempotency key & request data
       More about idempotent request: https://developer.paypal.com/docs/platforms/develop/idempotency/
    """
    pass
