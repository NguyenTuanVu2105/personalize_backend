import logging

from django.db.models import Prefetch

from abstract_product.models import AbstractProductVariant, ProductAttributeValue, ProductAttribute
from abstract_product.serializers.abstract_product_variant import ProductVariantPriceSerializer, \
    ProductVariantPriceAttributeSerializer
from shipping.models import ShippingCostAbstractVariant, ShippingZone, ShippingRate
from shipping.serializers import BriefShippingRateSerializer
from shipping.serializers.shipping_zone_serializer import BriefShippingZoneSerializer

logger = logging.getLogger(__name__)


def variants_handler(variants):
    variant_dicts = dict(map(lambda v: (v.sku, v), variants))
    shipping_costs = ShippingCostAbstractVariant.objects \
        .only("abstract_variant_sku", "shipping_cost_base", "shipping_cost_additional", "production_cost_base",
              "production_cost_additional", "shipping_zone", "shipping_rate") \
        .filter(abstract_variant_sku__in=variant_dicts.keys())
    for shipping_cost in shipping_costs:
        variant_sku = shipping_cost.abstract_variant_sku
        variant = variant_dicts.get(variant_sku)
        if hasattr(variant, 'shipping_costs'):
            variant.shipping_costs.append(shipping_cost)
        else:
            variant.shipping_costs = [shipping_cost]

    if not shipping_costs:
        for variant in variants:
            variant.shipping_costs = []

    return variants


def retrieve_product_pricing(product_id):
    variants = AbstractProductVariant.objects \
        .only('id', 'sku') \
        .filter(product_id=product_id).all()
    variants = variants_handler(variants)
    shipping_zones = ShippingZone.objects.all().only("id", "name", "description")
    shipping_rates = ShippingRate.objects.all().only("id", "name", "description")

    return {
        "costs": ProductVariantPriceSerializer(instance=variants, many=True).data,
        "shipping_zones": BriefShippingZoneSerializer(instance=shipping_zones, many=True).data,
        "shipping_rates": BriefShippingRateSerializer(instance=shipping_rates, many=True).data
    }


def retrieve_pricing_with_attributes(variant_id):
    variants = AbstractProductVariant.objects \
        .prefetch_related(
        Prefetch('attributes_value', queryset=ProductAttributeValue.objects.only('id', 'label').filter(is_active=True)),
        Prefetch('attributes_value__attribute',
                 queryset=ProductAttribute.objects.only('id', 'name').filter(is_active=True))) \
        .only('id', 'sku', 'attributes_value', 'attributes_value__attribute') \
        .filter(id=variant_id)

    variants = variants_handler(variants)

    return ProductVariantPriceAttributeSerializer(instance=variants, many=True).data[0]


def get_min_product_cost(abstract_variant, shop, extra_cost):
    shipping_cost = ShippingCostAbstractVariant.objects \
        .only("abstract_variant_sku", "production_cost_base").filter(
        abstract_variant_sku=abstract_variant.sku).order_by("production_cost_base").first()
    currency = shop.currency
    return float(round((shipping_cost.production_cost_base + extra_cost) * currency.rate, currency.precision))
