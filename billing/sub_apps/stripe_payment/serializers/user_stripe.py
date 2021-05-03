from rest_framework import serializers

from ..models import UserStripe


class UserStripeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStripe
        fields = ('id', 'user', 'customer_code', 'type', 'create_time', 'update_time')
