from rest_framework.response import Response

from HUB.views import APIView


class GetClientIP(APIView):
    @staticmethod
    def get(request):
        fields = ['HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR', 'HTTP_X_REAL_IP']
        data = {field: request.META.get(field) for field in fields}
        return Response(data)
