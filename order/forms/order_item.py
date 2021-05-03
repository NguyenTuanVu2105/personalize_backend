import logging

from django.forms import ValidationError

from HUB import settings
from HUB.forms.base import ModelForm
from order.constants.mapping_statuses import MappingStatus
from order.models import OrderItem
from shop.constants.shop_status import ShopStatus
from shop.models import Shop
from user_product.constants import UserProductStatus
from user_product.models import UserVariant, EcommerceUnsyncVariant

logger = logging.getLogger(__name__)


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order_pack", "order", "item_id", "quantity", "price", "discount", "currency", "user_variant",
                  "mfr_base_cost", "mapping_status", "ecommerce_variant"]
        optional_fields = ["user_variant", "mfr_base_cost"]

    def get_user_variant(self, sku):
        logger.info(sku)
        if sku is None or len(sku) == 0:
            return None
        shop = Shop.objects.filter(url=self.data.get("shop_url"), status=ShopStatus.ACTIVE).first()
        return UserVariant.objects.filter(sku=sku,
                                          user_product__status=UserProductStatus.ACTIVE,
                                          user_product__shop=shop,
                                          user_product__user=shop.owner
                                          ).first()

    def get_user_ecommerce_variant(self, sku):
        return EcommerceUnsyncVariant.objects.filter(sku=sku).first()

    def update_mapping_status(self):
        if self.data.get("vendor") == settings.PRODUCT_VENDOR_NAME:
            self.instance.mapping_status = MappingStatus.UNMAPPED

    def clean_user_variant(self):
        # todo validate whether user variant is owned by shop
        sku = self.data.get("sku") or (self.instance.user_variant.sku if self.instance.user_variant else None)
        if not sku:
            raise ValidationError("No variant sku")
        user_variant = self.get_user_variant(sku=sku)
        if user_variant is None:
            raise ValidationError("Invalid variant sku")
        # if user_variant is None:
        #     ecommerce_variant = self.get_user_ecommerce_variant(sku=self.data.get("sku"))
        #     if ecommerce_variant is None:
        #         raise ValidationError("Invalid variant sku")
        #     self.instance.ecommerce_variant = ecommerce_variant
        #     user_variant = ecommerce_variant.user_variant
        #     if not user_variant:
        #         self.update_mapping_status()
        return user_variant

    def save(self, commit=True):
        return super().save()


class SampleOrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "item_id", "quantity", "price", "currency", "user_variant", "mapping_status"]
        optional_fields = ["user_variant"]

    def get_user_variant(self, ):
        return UserVariant.objects.get(pk=self.data.get("user_variant_id"))

    def get_user_ecommerce_variant(self, sku):
        return EcommerceUnsyncVariant.objects.filter(sku=sku).first()

    def update_mapping_status(self):
        if self.data.get("vendor") == settings.PRODUCT_VENDOR_NAME:
            self.instance.mapping_status = MappingStatus.UNMAPPED

    def clean_user_variant(self):
        user_variant = self.get_user_variant()
        return user_variant

    def save(self, commit=True):
        return super().save()


class UserOrderItemUpdateForm(OrderItemForm):
    class Meta(OrderItemForm.Meta):
        fields = ["quantity", "user_variant", "mfr_base_cost", "price"]
        optional_fields = ["quantity", "user_variant", "mfr_base_cost", "price"]

    def get_user_variant(self, sku):
        return UserVariant.objects.get(user_product_id=self.instance.user_variant.user_product_id, sku=sku)

    def clean_price(self):
        user_variant = self.get_user_variant(self.data['sku'])
        shop = self.instance.order.shop
        is_order_sample = shop.ecommerce.name == "PrintHolo"
        if is_order_sample:
            user_variant_price = user_variant.prices.filter(currency=shop.currency.currency).first()
            return user_variant_price.value
        else:
            return self.instance.price


class BrandingCardOrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order_pack", "order", "item_id", "price", "currency", "user_variant", "mapping_status"]
        optional_fields = ["user_variant", "mfr_base_cost", "quantity", "discount", "ecommerce_variant",
                           "mapping_status"]

    def save(self, commit=True):
        return super().save()
