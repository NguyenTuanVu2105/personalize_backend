from django.contrib import admin

from user_product.models import UserVariantPrice, ArtworkFusionInfo, ArtworkFusion
from .models import UserProductArtworkFusion, UserProduct, UserVariant, Artwork, UserVariantSideMockup, ShopUserProduct


@admin.register(UserVariantSideMockup)
class UserVariantSideMockupAdmin(admin.ModelAdmin):
    list_display = ('user_variant', 'mockup_url')


@admin.register(UserProductArtworkFusion)
class UserProductArtworkFusionAdmin(admin.ModelAdmin):
    list_display = ('user_product', 'product_side', 'artwork_fusion')


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'original_image_path', 'is_public', 'sha256', 'create_time', 'update_time')


@admin.register(ArtworkFusion)
class ArtworkFusionAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'original_image_path', 'create_time', 'update_time')


@admin.register(ArtworkFusionInfo)
class ArtworkFusionInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'frame', 'layer', 'rotation', 'position', 'scale')


@admin.register(UserProduct)
class UserProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'description', 'user', 'abstract_product', 'preview_image_url', 'create_time', 'update_time')


@admin.register(UserVariant)
class UserVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_product', 'abstract_variant', 'sku', 'create_time', 'update_time')


@admin.register(ShopUserProduct)
class ShopUserProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_product', 'shop', 'sync_status', 'sync_status_message', 'create_time', 'update_time')


@admin.register(UserVariantPrice)
class UserVariantPriceAdmin(admin.ModelAdmin):
    list_display = ["user_variant", "currency", "value", "update_time"]
