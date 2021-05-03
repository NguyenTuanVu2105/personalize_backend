import logging

from rest_framework.response import Response

from HUB.functions import get_client_ip
from HUB.views import APIView
from service_communication.services import save_shop

logger = logging.getLogger(__name__)


class ShopifyBridge(APIView):
    error_messages = {
        "shop": {
            "required": "The shop field is required",
        },
        "code": {
            "required": "The code field is required",
        },
    }

    def post(self, request):
        request_data = request.data
        client_ip = get_client_ip(request)
        success, response = save_shop(request_data['shop'], request_data['code'], self.request.user, client_ip=client_ip)

        return Response({"success": success, "data": response})
