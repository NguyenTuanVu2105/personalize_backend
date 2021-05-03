from rest_framework import serializers
from rest_framework.fields import IntegerField

from abstract_product.serializers import ProductAttributeSerializer
from abstract_product.serializers.abstract_product_meta import AbstractProductMetaForSampleProductSerializer
from user_product.models import SampleProduct


class SampleProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleProduct
        fields = ('id', 'original_product', 'title', 'preview_image_url')


class AdminSampleProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleProduct
        fields = (
            'id', 'original_product', 'title', 'preview_image_url', 'status', 'create_time', 'update_time',
            "create_time", 'detail_data', 'is_highlight', 'last_refresh_data_time')


class AdminSampleProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleProduct
        fields = ('id', 'original_product', 'title', 'preview_image_url', 'is_highlight')


class SampleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleProduct
        fields = ('id', 'original_product', 'detail_data')


class PopularSampleProductSerializer(serializers.ModelSerializer):
    total_created = IntegerField()
    total_sold = IntegerField()

    class Meta:
        model = SampleProduct
        fields = ('id', 'title', 'total_created', 'total_sold')


class DetailSampleProductWithAbstractSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, source="original_product.abstract_product.child_attributes")
    abstract_meta = AbstractProductMetaForSampleProductSerializer(read_only=True,
                                                                  source="original_product.abstract_product.meta")
    abstract_sku = serializers.StringRelatedField(source="original_product.abstract_product.sku")

    class Meta:
        model = SampleProduct
        fields = ('id', 'detail_data', 'attributes', 'abstract_meta', 'abstract_sku')
