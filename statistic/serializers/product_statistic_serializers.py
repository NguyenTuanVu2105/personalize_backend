from rest_framework.serializers import ModelSerializer

from statistic.models import AbstractProductStatistic


class ProductStatisticSerializer(ModelSerializer):
    class Meta:
        model = AbstractProductStatistic
        fields = '__all__'
