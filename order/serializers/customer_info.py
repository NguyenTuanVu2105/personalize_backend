from rest_framework.serializers import ModelSerializer

from order.models import CustomerInfo


class CustomerInfoSerializer(ModelSerializer):
    class Meta:
        model = CustomerInfo
        fields = ["id", "customer_id", "first_name", "last_name", "email", "phone"]
