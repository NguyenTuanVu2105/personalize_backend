from django.contrib import admin

from .models import (
    AbstractProduct, AbstractProductVariant, AbstractProductCategory, ProductAttribute, ProductAttributeValue,
    AbstractProductVariantAttribute,
    AbstractProductSide, AbstractProductMeta, CategoryProduct, AbstractProductMockupInfo)


@admin.register(AbstractProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'preview_image_url', 'sort_index')


@admin.register(AbstractProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", 'title', 'is_active', 'preview_image_url')


@admin.register(CategoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ("id", 'category', 'product')


@admin.register(AbstractProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'sku', 'description')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'type')


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute', 'label', 'value', 'sort_index')


@admin.register(AbstractProductVariantAttribute)
class AbstractProductVariantAttributeAdmin(admin.ModelAdmin):
    list_display = ('variant', 'attribute_value')


@admin.register(AbstractProductMeta)
class AbstractProductMetaAdmin(admin.ModelAdmin):
    list_display = ('abstract_product', 'default_variant', 'description', 'short_description', 'shipping_meta', 'base_cost', 'pricing_meta')


@admin.register(AbstractProductSide)
class AbstractProductSideAdmin(admin.ModelAdmin):
    list_display = ('id', 'abstract_product', 'type', 'constraints', 'fusion_size', 'create_time', 'update_time')


@admin.register(AbstractProductMockupInfo)
class AbstractProductMockupInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'abstract_product', 'name', 'meta', 'create_time', 'update_time')
