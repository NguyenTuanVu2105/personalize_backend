from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from abstract_product.models import AbstractProduct
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer


class HealthCheckViewSet(ViewSet):
    authentication_classes = {}
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]

    @action(methods=["GET"], detail=False, url_path="liveness")
    def liveness(self, request):
        return Response()

    @action(methods=["GET"], detail=False, url_path="started")
    def started(self, request):
        abstract_product = AbstractProduct.objects.first()
        data = BriefAbstractProductSerializer(abstract_product).data
        return Response(data)

    @action(methods=["GET"], detail=False, url_path="readiness")
    def readiness(self, request):
        abstract_product = AbstractProduct.objects.first()
        data = BriefAbstractProductSerializer(abstract_product).data
        return Response(data)
