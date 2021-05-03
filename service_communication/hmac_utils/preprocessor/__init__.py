from HUB.settings import HMAC_FULFILL_WEBHOOK_REQUEST_HEADER
from .hmac_message_handler import fulfillment_message_handler
from .hmac_signature_handler import fulfillment_signature_handler


class HmacPreprocessor:
    def __init__(self, message_handler, signature_handler):
        self.message_handler = message_handler
        self.signature_handler = signature_handler

    def obtain_key_pair(self, request):
        return self.message_handler(request), self.signature_handler(request)

    @staticmethod
    def obtain_header(request):
        return request.headers.get(HMAC_FULFILL_WEBHOOK_REQUEST_HEADER)


hmac_fulfill_preprocessor = HmacPreprocessor(fulfillment_message_handler, fulfillment_signature_handler)
