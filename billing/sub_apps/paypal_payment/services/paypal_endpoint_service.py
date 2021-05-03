from HUB import settings

API_V1 = settings.PAYPAL_APP_API_V1
API_V2 = settings.PAYPAL_APP_API_V2


class PaypalEndpointService:
    # authorization
    GET_ACCESS_TOKEN_ENDPOINT = f'{API_V1}/oauth2/token'

    # customer
    GENERATE_CUSTOMER_TOKEN = f'{API_V1}/identity/generate-token'

    # order
    CHECKOUT_ORDER = f'{API_V2}/checkout/orders'
    CAPTURE_ORDER = f'{API_V2}/checkout/orders/{{order_id}}/capture'
    GET_CAPTURE_DETAIL = f'{API_V2}/payments/captures/{{capture_id}}'
    GET_ORDER_DETAIL = f'{API_V2}/checkout/orders/{{order_id}}'

    # payment token
    BASE_PAYMENT_TOKEN = f'{API_V2}/vault/payment-tokens'
    LIST_PAYMENT_TOKEN_BY_CUSTOMER_ID = f'{BASE_PAYMENT_TOKEN}'
    GET_PAYMENT_TOKEN_DETAIL = f'{BASE_PAYMENT_TOKEN}/{{token_id}}'

    # billing-agreement
    CREATE_BILLING_AGREEMENT_ENDPOINT = f'{API_V1}/billing-agreements/agreement-tokens'
    ACTIVATE_BILLING_AGREEMENT_ENDPOINT = f'{API_V1}/billing-agreements/agreements'
    CANCEL_BILLING_AGREEMENT_ENDPOINT = f'{API_V1}/billing-agreements/agreements/{{agreement_id}}/cancel'

    # charge
    CREATE_PAYMENT_ENDPOINT = f'{API_V1}/payments/payment'
    GET_SALE_DETAIL_ENDPOINT = f'{API_V1}/payments/sale/{{sale_id}}'
    GET_PAYMENT_DETAIL_ENDPOINT = f'{CREATE_PAYMENT_ENDPOINT}/{{payment_id}}'

    # refund
    REFUND_SALE_ENDPOINT = f'{API_V1}/payments/sale/{{sale_id}}/refund'
    REFUND_ORDER_ENDPOINT = f'{API_V2}/payments/captures/{{capture_id}}/refund'
