from rest_framework import serializers

from user_product.models import UserProduct, Artwork, ArtworkFusion, ArtworkFusionInfo, UserProductArtworkFusion, \
    UserVariant, UserVariantArtworkFusion, UserVariantPrice, UserVariantSideMockup, TextPersonalization


class SPArtworkSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    artwork_default = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Artwork
        fields = ('id', 'owner', 'artwork_default', 'name', 'file_url', 'original_image_path', 'thumbnail_image_path',
                  'is_public', 'status', 'width', 'height',
                  'sha256', 'last_used_time', 'total_created_product', 'is_default')


class SPLayerContentSerializer(serializers.RelatedField):
    def to_representation(self, layer_content):
        if isinstance(layer_content, Artwork):
            serializer_data = SPArtworkSerializer(instance=layer_content).data

        elif isinstance(layer_content, TextPersonalization):
            from user_product.serializers import DetailTextPersonalizationSerializer
            serializer_data = DetailTextPersonalizationSerializer(instance=layer_content).data

        else:
            raise Exception('Unexpected type of tagged object')

        return serializer_data

    def to_internal_value(self, data):
        pass


class SPArtworkFusionInfoSerializer(serializers.ModelSerializer):
    # artwork = SPArtworkSerializer()
    frame = serializers.PrimaryKeyRelatedField(read_only=True)
    layer_content = SPLayerContentSerializer(read_only=True)

    class Meta:
        model = ArtworkFusionInfo
        fields = ('frame', 'layer', 'rotation', 'position', 'scale', 'dnd_scale', 'is_hidden', 'layer_content',
                  'layer_type')


class SPArtworkFusionSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    artwork_fusion_info_data = SPArtworkFusionInfoSerializer(source='artwork_fusion_info_artwork_set', many=True)

    class Meta:
        model = ArtworkFusion
        fields = ('name', 'owner', 'original_image_path', 'image_url', 'background_color', 'artwork_fusion_info_data')


class SPUserProductArtworkFusionSerializer(serializers.ModelSerializer):
    user_product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_side = serializers.PrimaryKeyRelatedField(read_only=True)
    artwork_fusion = SPArtworkFusionSerializer()

    class Meta:
        model = UserProductArtworkFusion
        fields = ('user_product', 'product_side', 'artwork_fusion', 'send_to_fulfill', 'is_seller_visible')


class SPUserVariantArtworkFusionSerializer(serializers.ModelSerializer):
    user_variant = serializers.PrimaryKeyRelatedField(read_only=True)
    variant_side = serializers.PrimaryKeyRelatedField(read_only=True)
    artwork_fusion = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserVariantArtworkFusion
        fields = ('user_variant', 'variant_side', 'artwork_fusion')


class SPUserVariantPriceSerializer(serializers.ModelSerializer):
    user_variant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserVariantPrice
        fields = ('user_variant', 'currency', 'value')


class SPUserVariantSideMockupSerializer(serializers.ModelSerializer):
    user_variant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserVariantSideMockup
        fields = ('user_variant', 'mockup_url', 'mockup_thumbnail_url')


class SPUserVariantSerializer(serializers.ModelSerializer):
    user_product = serializers.PrimaryKeyRelatedField(read_only=True)
    abstract_variant = serializers.PrimaryKeyRelatedField(read_only=True)

    user_variant_price_data = SPUserVariantPriceSerializer(source='prices', many=True)
    user_variant_side_mockup_data = SPUserVariantSideMockupSerializer(source='mockup_per_side', many=True)
    user_variant_artwork_fusion_data = SPUserVariantArtworkFusionSerializer(source='user_variant_artwork_set',
                                                                            many=True)

    class Meta:
        model = UserVariant
        fields = ('user_product', 'abstract_variant', 'sku', 'sort_index', 'is_active', 'user_variant_price_data',
                  'user_variant_side_mockup_data', 'user_variant_artwork_fusion_data')


class SPUserProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    abstract_product = serializers.PrimaryKeyRelatedField(read_only=True)
    # user_product_artwork_fusion_data = serializers.SerializerMethodField('get_user_product_artwork_fusion')
    user_product_artwork_fusion_data = SPUserProductArtworkFusionSerializer(source='artwork_set', many=True)
    user_variant_data = SPUserVariantSerializer(source='user_product_variant_set', many=True)

    # def get_user_product_artwork_fusion(self, user_product):
    #     # qs = UserProductArtworkFusion.objects.is_visible().filter(user_product=user_product)
    #     qs = user_product.artwork_set.is_visible()
    #     serializer = SPUserProductArtworkFusionSerializer(instance=qs, many=True)
    #     return serializer.data

    class Meta:
        model = UserProduct
        fields = ('user', 'abstract_product', 'preview_image_url', 'title', 'description', 'status', 'extra_cost',
                  'user_product_artwork_fusion_data', 'user_variant_data', 'background_color')
