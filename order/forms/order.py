import logging

from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError, forms

from HUB.forms.base import ModelForm
from order.models import Order
from shipping.models import ShippingRate
from shop.constants.shop_status import ShopStatus
from shop.models import Shop, ShopShippingRateMapping

logger = logging.getLogger(__name__)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["order_id", "order_number", "note", "total_price", "currency", "customer_info",
                  "shipping_address", "shop", "tags", "e_commerce_shipping_lines", "shipping_rate",
                  "total_items", "seller_edit_time"]
        optional_fields = ["shop", "order_number", "e_commerce_shipping_lines", "shipping_rate"]

    def clean_shop(self):
        try:
            shop = Shop.objects.filter(url=self.data.get("shop_url"), status=ShopStatus.ACTIVE).first()
        except Shop.DoesNotExist:
            raise ValidationError("Invalid shop url")
        return shop

    # def clean_edit_order_items_delay(self):
    #     try:
    #         shop = Shop.objects.filter(url=self.data.get("shop_url"), status=ShopStatus.ACTIVE).first()
    #         owner_settings = shop.owner.settings
    #         edit_order_items_delay = owner_settings.edit_order_items_delay
    #     except Shop.DoesNotExist:
    #         raise ValidationError("Invalid shop url")
    #     except Exception as e:
    #         raise ValidationError(str(e))
    #     return edit_order_items_delay
    #
    # def clean_request_order_processing_manually(self):
    #     try:
    #         shop = Shop.objects.filter(url=self.data.get("shop_url"), status=ShopStatus.ACTIVE).first()
    #         owner_settings = shop.owner.settings
    #         request_order_processing_manually = owner_settings.request_order_processing_manually
    #     except Shop.DoesNotExist:
    #         raise ValidationError("Invalid shop url")
    #     except Exception as e:
    #         raise ValidationError(str(e))
    #     return request_order_processing_manually

    def clean_shipping_rate(self):
        try:
            shipping_lines = list(map(lambda shipping_line: shipping_line["title"], self.data.get("shipping_lines")))
            country = self.data.get("country_code")
            shipping_rate_mapping = ShopShippingRateMapping.objects. \
                filter(shop__url=self.data.get("shop_url"),
                       e_commerce_shipping_rate_name__in=shipping_lines,
                       countries__contains=[country]).first()
            if shipping_rate_mapping is None:
                shipping_rate_mapping = ShopShippingRateMapping.objects. \
                    filter(shop__url=self.data.get("shop_url"),
                           e_commerce_shipping_rate_name__in=shipping_lines,
                           countries__contains=["*"]).first()

            if shipping_rate_mapping is None:
                shipping_rate = ShippingRate.objects.filter(is_default=True).first()
            else:
                shipping_rate = shipping_rate_mapping.shipping_rate
        except ObjectDoesNotExist:
            shipping_rate = None
        self.data.update(shipping_rate=shipping_rate)
        return shipping_rate

    def clean_e_commerce_shipping_lines(self):
        shipping_line = self.data.get("shipping_lines")
        self.data.update(e_commerce_shipping_lines=shipping_line)
        return shipping_line


class SampleOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["note", "total_price", "currency", "customer_info",
                  "shipping_address", "shipping_rate",
                  "total_items", "type", "shop", "order_id", "order_number", "seller_edit_time"]
        optional_fields = ["order_id", "order_number"]

    def clean(self):
        if not self.cleaned_data['shop']:
            raise forms.ValidationError('Invalid shop!')


class OrderShippingRateUpdateForm(ModelForm):
    class Meta(OrderForm.Meta):
        fields = ["shipping_rate"]
        optional_fields = []
