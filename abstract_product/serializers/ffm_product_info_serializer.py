from rest_framework.serializers import ModelSerializer

from abstract_product.models.ffm_product_infos import FFMProductInfo


class FFMProductInfoSerializer(ModelSerializer):
    class Meta:
        model = FFMProductInfo
        fields = '__all__'
