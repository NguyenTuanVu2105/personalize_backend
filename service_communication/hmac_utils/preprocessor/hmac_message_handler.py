import json

from HUB.settings import HMAC_FULFILL_WEBHOOK_REQUEST_HEADER


def fulfillment_message_handler(request, *args, **kwargs):
    fulfill_signature = dict(map(lambda s: s.split('='), request.headers.get(HMAC_FULFILL_WEBHOOK_REQUEST_HEADER)
                                 .split(',')))
    timestamp = fulfill_signature.get('t')
    payload = json.dumps(request.data, separators=(',', ':'))

    return f'{timestamp}.{payload}'
