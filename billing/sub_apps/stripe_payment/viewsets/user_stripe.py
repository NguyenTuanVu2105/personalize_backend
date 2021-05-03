from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .base import AuthenticatedModelViewSet
from ..models import UserStripe
from ..serializers import UserStripeSerializer


class UserStripeViewSet(AuthenticatedModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = UserStripe.objects.all().order_by('-create_time')
    serializer_class = UserStripeSerializer
    filterset_fields = ['id', 'user', 'customer_code', 'type', ]
    search_fields = ['id', 'user__id', 'customer_code', 'type', ]
    ordering_fields = ['id', 'user', 'customer_code', 'type', 'create_time', 'update_time']

    def destroy(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            card = UserStripe.objects.get(id=id)
            card.delete()
        except Exception as e:
            return Response({"success": False, "message": str(e)})
        else:
            return Response({"success": True, "message": "This card have been deleted"})
