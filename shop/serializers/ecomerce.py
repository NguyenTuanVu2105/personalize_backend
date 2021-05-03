from rest_framework.serializers import ModelSerializer

from shop.models import Ecommerce


class EcommerceSerializer(ModelSerializer):
    class Meta:
        model = Ecommerce
        fields = ['name', 'description']


class BriefEcommerceSerializer(ModelSerializer):
    class Meta:
        model = Ecommerce
        fields = ['name']
