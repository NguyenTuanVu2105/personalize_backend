# from rest_framework import viewsets
# from rest_framework.response import Response
#
# from shipping.models import ShippingProfileDefault
# from shipping.serializers.shiping_profile_default import BriefShippingProfileSerializer
#
#
# class AdminShippingProfileDefaultViewSet(viewsets.ModelViewSet):
#     queryset = ShippingProfileDefault.objects.all()
#     serializer_class = BriefShippingProfileSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         return Response(self.serializer_class(queryset, many=True).data)
