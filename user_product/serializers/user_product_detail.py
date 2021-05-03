from django.db.models import Count, Sum
from rest_framework import serializers

from abstract_product.models import AbstractProductVariant, ProductAttributeValue, ProductAttribute
from abstract_product.serializers import ProductBasicInfoSerializer
from abstract_product.serializers.brief_abstract_product import BriefAbstractProductSerializer
from user_product.functions import retrieve_user_product_variant_with_pricing
from user_product.models import UserVariant, UserProduct, ShopUserProduct
from user_product.serializers import UserVariantSideMockupSerializer, ShopUserProductSerializer
from user_product.serializers.user_product_artwork_fusion import DetailUserProductSideArtworkFusionSerializer
from user_product.serializers.user_variant_artwork_fusion import DetailUserVariantSideArtworkFusionSerializer
from user_product.serializers.user_variant_price import BriefUserVariantPriceSerializer


class BriefShopSerializer(serializers.ModelSerializer):
    ecommerce = serializers.CharField(source='shop.ecommerce.name')
    name = serializers.CharField(source='shop.name')
    url = serializers.CharField(source='shop.url')
    currency = serializers.CharField(source='shop.currency')

    class Meta:
        model = ShopUserProduct
        fields = ('id', 'name', 'url', 'ecommerce', 'currency')


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.StringRelatedField(source='attribute.to_string')

    class Meta:
        model = ProductAttributeValue
        fields = ('id', 'label', 'value', 'attribute', 'attribute_name', 'sort_index')


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes_value = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = AbstractProductVariant
        fields = ('id', 'product', 'sku', 'description', 'attributes_value')


class ProductVariantEcommerceSerializer(ProductVariantSerializer):
    product = ProductBasicInfoSerializer()

    class Meta(ProductVariantSerializer.Meta):
        fields = ('id', 'product', 'sku', 'description', 'attributes_value')


class UserVariantSerializerPrice(serializers.ModelSerializer):
    mockup_per_side = UserVariantSideMockupSerializer(many=True)
    abstract_variant = ProductVariantSerializer()
    prices = BriefUserVariantPriceSerializer(many=True)

    class Meta:
        model = UserVariant
        fields = ('id', "sku", 'abstract_variant', 'mockup_per_side', 'prices', 'sort_index')


class BriefUserVariantSerializer(serializers.ModelSerializer):
    prices = BriefUserVariantPriceSerializer(many=True)

    class Meta:
        model = UserVariant
        fields = ('id', 'prices', 'sort_index', 'type')


class AdminUserVariantSerializerPrice(UserVariantSerializerPrice):
    cost = serializers.SerializerMethodField()

    def get_cost(self, instance):
        from shipping.models import ShippingCostAbstractVariant
        shipping_costs = ShippingCostAbstractVariant.objects.filter(abstract_variant_sku=instance.abstract_variant.sku)
        if shipping_costs.count() > 0:
            return shipping_costs.first().production_cost_base
        else:
            return 0

    class Meta(UserVariantSerializerPrice.Meta):
        model = UserVariant
        fields = ('id', "sku", 'abstract_variant', 'mockup_per_side', 'prices', 'sort_index', 'cost')


class UserVariantEcommerceSerializer(serializers.ModelSerializer):
    abstract_variant = ProductVariantEcommerceSerializer()
    prices = BriefUserVariantPriceSerializer(many=True)
    side_artworks = DetailUserVariantSideArtworkFusionSerializer(source='user_variant_artwork_set', many=True)

    class Meta:
        model = UserVariant
        fields = ('id', "sku", 'abstract_variant', 'prices', 'sort_index', 'side_artworks')


class ProductAttributeSerializer(serializers.ModelSerializer):
    child_attributes_value_set = ProductAttributeValueSerializer(many=True)

    class Meta:
        model = ProductAttribute
        fields = ("id", "product", "name", "type", "child_attributes_value_set")


class UserProductDetailSerializer(serializers.ModelSerializer):
    user_product_variant_set = UserVariantSerializerPrice(many=True)
    shop_user_product_set = ShopUserProductSerializer(many=True)
    child_attributes_data = ProductAttributeSerializer(source="abstract_product.child_attributes", many=True)
    shops = BriefShopSerializer(source='shop_user_product_set', many=True)
    side_artworks = DetailUserProductSideArtworkFusionSerializer(source='artwork_set', many=True)
    abstract_product = BriefAbstractProductSerializer()
    order_item_count = serializers.SerializerMethodField()

    def get_order_item_count(self, object):
        return object.user_product_variant_set.all().aggregate(order_items__quantity=Sum('order_items__quantity'),
                                                               order_items__count=Count('order_items'))

    class Meta:
        model = UserProduct
        fields = (
            'id', 'user', 'order_item_count', 'shop_user_product_set', 'title', 'description', 'abstract_product',
            'preview_image_url', 'create_time',
            'status', 'update_time', 'user_product_variant_set', 'child_attributes_data', 'shops',
            'side_artworks', 'combine_fusion')


# class ProductVariantWithoutProductInfoSerializer(ProductVariantSerializer):
#     # use in create Order Sample, please deal with it if you want to edit
#     # prices = BriefUserVariantPriceSerializer(many=True)
#     attributes_value = ProductAttributeValueSerializer(source="abstract_variant.attributes_value", many=True)
#     price = serializers.SerializerMethodField()
#     def get_price(self, object):
#         price_object = object.prices.filter(currency=DEFAULT_CURRENCY).first()
#         if price_object:
#             return price_object.value
#         else:
#             return 0.0
#
#     class Meta:
#         model = UserVariant
#         fields = ('id', 'sku', 'attributes_value', 'price')


class BriefUserProductSerializer(serializers.ModelSerializer):
    # use in create Order Sample, please deal with it if you want to edit

    class Meta:
        model = UserProduct
        fields = ('id', 'title', 'preview_image_url')


class UserProductWithVariantsSerializer(serializers.ModelSerializer):
    user_variants = serializers.SerializerMethodField()

    @staticmethod
    def get_user_variants(instance):
        return retrieve_user_product_variant_with_pricing(instance)

    class Meta:
        model = UserProduct
        fields = ('id', 'title', 'preview_image_url', 'user_variants')
