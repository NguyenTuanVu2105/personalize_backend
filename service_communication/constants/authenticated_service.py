class AuthenticatedService:
    FRESH_DESK_WEBHOOK = 'fresh_desk_webhook'
    ECOMMERCE_ADAPTER = 'ecommerce_adapter'
    FULFILLMENT = 'fulfillment'


class VerboseAuthenticatedService:
    FRESH_DESK_WEBHOOK = 'fresh_desk_webhook'
    ECOMMERCE_ADAPTER = 'ecommerce_adapter'
    FULFILLMENT = 'fulfillment'


AUTHENTICATION_SERVICE_TYPES = [
    (AuthenticatedService.FRESH_DESK_WEBHOOK, VerboseAuthenticatedService.FRESH_DESK_WEBHOOK),
    (AuthenticatedService.ECOMMERCE_ADAPTER, VerboseAuthenticatedService.ECOMMERCE_ADAPTER),
    (AuthenticatedService.FULFILLMENT, VerboseAuthenticatedService.FULFILLMENT),
]
