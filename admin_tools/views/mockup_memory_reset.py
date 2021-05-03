import json

import os
import logging
import requests
from rest_framework.response import Response

from HUB.viewsets.base import AdminGenericAPIView

logger = logging.getLogger(__name__)
RESET_MOCKUP_MEMORY_PATH = os.environ.get("RESET_MOCKUP_MEMORY_PATH")


class MockupMemoryReset(AdminGenericAPIView):
    @staticmethod
    def post(request):
        request_data = request.data
        url = RESET_MOCKUP_MEMORY_PATH
        try:
            re = requests.post(url=url, json=request_data)
            reset_response = json.loads(re.text)
            if reset_response['success']:
                return Response({"success": reset_response['success'], "message": "Reset mockup memory successfully"})
            else:
                return Response(reset_response)

        except Exception as e:
            print(str(e))
            return Response({"success": False, "message": str(e)})


