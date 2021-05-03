from HUB.settings import HMAC_FULFILL_WEBHOOK_REQUEST_HEADER


def fulfillment_signature_handler(request):
    fulfill_signature = dict(map(lambda s: s.split('='), request.headers.get(HMAC_FULFILL_WEBHOOK_REQUEST_HEADER).split(',')))
    return fulfill_signature.get('v1')
