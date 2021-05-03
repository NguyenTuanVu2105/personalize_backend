from rest_framework import serializers

from user_product.models import UserVariantPrice


class BriefUserVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVariantPrice
        fields = ('id', 'currency', "value")
