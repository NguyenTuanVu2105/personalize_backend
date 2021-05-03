from rest_framework.serializers import ModelSerializer

from statistic.models import ShippingTimeStatistic


class ShippingTimeStatisticSerializer(ModelSerializer):
    class Meta:
        model = ShippingTimeStatistic
        fields = '__all__'
